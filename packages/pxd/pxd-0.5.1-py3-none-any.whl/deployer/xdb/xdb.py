#   Copyright [2013-2021], Alibaba Group Holding Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import json
import logging
import os
import random
import secrets
import string
from pathlib import Path

from retrying import retry

import deployer.constant.constant as constant
import deployer.core.docker_manager as DockerManager
from deployer._repo import pxd_working_dir
from deployer.config.config import Config
from deployer.core.flow import Flow
from deployer.decorator.decorators import xdb_create_task
from deployer.sqlite import dbapi
from deployer.util.file_manager import FileManager

XDB_ALL_ROLES = ["Leader", "Follower", "Logger", "Learner", "Candidate", "Voter"]
XDB_REQUIRED_ROLES = ["Leader", "Follower", "Logger"]


def retry_if_result_none(result):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    return result is None


def _generate_container_role(role):
    """Return container role for container, which is passed to container as env: ROLE_POD"""
    if role in ("Leader", "Follower"):
        return "candidate"
    else:
        return "voter"


logger = logging.getLogger(__name__)


class Xdb:
    existing_pots = {}

    def __init__(self, name, pxc_name, xdb_type, version, engine_image=None, hosts=['127.0.0.1'],
                 leader_only=True, cpu_limit=1,
                 mem_limit='2147483648',
                 engine_type='galaxy',
                 engine_version='8.0',
                 cpusets=["", "", ""],
                 memsets=["", "", ""],
                 no_logger=False):
        self.name = name
        self.pxc_name = pxc_name
        self.xdb_type = xdb_type
        self.engine_type = engine_type
        self.engine_version = engine_version
        self.version = version
        self.engine_image = Config.instance().dn_image if engine_image is None else engine_image
        self.hosts = hosts
        self.nodes = []
        self.leader_only = leader_only
        self.user_name = None
        self.password = None
        self.status = None
        self.error = None
        self.leader_node = None
        self.leader_cnt = 0
        self.cpu_limit = cpu_limit
        self.mem_limit = mem_limit
        self.cpusets = cpusets
        self.memsets = memsets
        self.no_logger = no_logger
        self.create_tasks = [
            self._pre_check_env,
            self._generate_topology,
            self._start_tool_container,
            self._copy_mycnf_template,
            self._start_xdb_container,
            self._wait_container_running,
            self._write_shared_channel,
            self._create_admin_account,
            self._finish_create_xdb
        ]

    def create(self):
        for idx, create_task in enumerate(self.create_tasks):
            result = create_task()
            if result == Flow.FAIL:
                break

    @xdb_create_task(task_name='finish create xdb')
    def _finish_create_xdb(self):
        self.status = 'running'

    @xdb_create_task(task_name='pre check')
    def _pre_check_env(self):
        for host in self.hosts:
            FileManager.mkdir(host, pxd_working_dir, exist_ok=True)
            FileManager.mkdir(host, f"{pxd_working_dir}/data/", exist_ok=True)
            FileManager.mkdir(host, f"{pxd_working_dir}/data/cache/xcluster-tools", exist_ok=True)
            shared_channel_file = f"{pxd_working_dir}/data/shared/{self.name}/shared-channel.json"
            if FileManager.exists(host, shared_channel_file):
                FileManager.remove(host, shared_channel_file)

        self.status = 'creating'

    @xdb_create_task(task_name='generate xdb topology')
    def _generate_topology(self):
        if len(self.hosts) == 1:
            role_list = XDB_REQUIRED_ROLES[:1] if self.leader_only else XDB_REQUIRED_ROLES
            for role in role_list:
                mysql_port = random.randint(14000, 18000)
                # TODO: retry while mysql_port not conflict
                while mysql_port in self.existing_pots:
                    mysql_port = random.random(14000, 18000)
                node = XdbNode(self.hosts[0], mysql_port, mysql_port + 8000, mysql_port + 28000, role,
                               cpusets=self.cpusets[0], memsets=self.memsets[0])
                node_type = 'Logger' if role == 'Logger' else 'Cand'
                node.name = self.name + '-' + node_type + '-' + str(mysql_port)
                self.nodes.append(node)
        elif len(self.hosts) == 3:
            role_list = XDB_REQUIRED_ROLES
            for i, role in enumerate(role_list):
                mysql_port = random.randint(14000, 18000)
                # TODO: retry while mysql_port not conflict
                while mysql_port in self.existing_pots:
                    mysql_port = random.random(14000, 18000)
                node = XdbNode(self.hosts[i], mysql_port, mysql_port + 8000, mysql_port + 28000, role,
                               cpusets=self.cpusets[i], memsets=self.memsets[i])
                node_type = 'Logger' if role == 'Logger' else 'Cand'
                node.name = self.name + '-' + node_type + '-' + str(i) + '-' + str(mysql_port)
                self.nodes.append(node)
            pass
        else:
            raise ValueError("hosts length is invalid, must be 1 or 3, current is: %s" % len(self.hosts))

    @xdb_create_task(task_name='wait container running')
    @retry(stop_max_attempt_number=20, wait_fixed=5000, retry_on_result=retry_if_result_none)
    def _wait_container_running(self):
        for node in self.nodes:
            client = DockerManager.get_client(node.host)
            container = client.containers.get(node.container_id)
            if container.status != 'running':
                return None
            node.container_ip = container.attrs['NetworkSettings']['IPAddress']

        return "True"

    @xdb_create_task(task_name='write shared channel files')
    def _write_shared_channel(self):
        shared_channel = {'nodes': []}
        for node in self.nodes:
            shared_channel['nodes'].append({
                "pod": node.name,
                "host": node.host if Config.instance().host_network_support() else node.container_ip,
                "port": node.paxos_port,
                "node_name": node.name,
                "role": node.role
            })
        shared_channel_file = f"{pxd_working_dir}/data/shared/{self.name}/shared-channel.json"
        for host in self.hosts:
            FileManager.write(host, shared_channel_file, json.dumps(shared_channel))

    @xdb_create_task(task_name='write pod info files')
    def _write_pod_info(self, node):
        node_id = node.host.replace('.', '_') + '_' + str(node.mysql_port)
        pod_info_dir = f'{pxd_working_dir}/data/podinfo/{node_id}'
        name_file = f'{pod_info_dir}/name'
        labels_file = f'{pod_info_dir}/labels'
        annotations_file = f'{pod_info_dir}/annotations'
        namespace_file = f'{pod_info_dir}/namespace'
        FileManager.write(node.host, name_file, node.name)
        FileManager.write(node.host, labels_file, '')
        FileManager.write(node.host, annotations_file, '')
        FileManager.write(node.host, namespace_file, '')

    @xdb_create_task(task_name='copy my.cnf')
    def _copy_mycnf_template(self):
        dst_file = pxd_working_dir + '/data/template/my.cnf.template'
        cur_dir = Path(os.path.dirname(os.path.realpath(__file__))).parent.absolute()
        src_file = f'{cur_dir}/resources/template/my.cnf-{self.engine_version}-{self.engine_type}'
        if os.path.exists(Config.instance().MYCNF_TEMPLATE):
            logger.info("use external my cnf: %s" % Config.instance().MYCNF_TEMPLATE)
            src_file = Config.instance().MYCNF_TEMPLATE

        for host in self.hosts:
            FileManager.copy(host, src_file=src_file, dst_file=dst_file)

    @xdb_create_task(task_name='copy scripts')
    def _start_tool_container(self):
        tools_dir = f'{pxd_working_dir}/data/cache/xcluster-tools'
        for node in self.nodes:
            client = DockerManager.get_client(node.host)
            logs = client.containers.run(Config.instance().dn_tool_image,
                                         ['/bin/ash', '-c', './hack/update.sh /target'],
                                         entrypoint='',
                                         remove=not Config.debug_mode_enabled(),
                                         privileged=True,
                                         stream=True,
                                         name=node.name + '-tool',
                                         volumes={
                                             tools_dir: {'bind': '/target', 'mode': 'rw'}},
                                         )
            logger.info("xstore tools logs")
            for log in logs:
                logger.info("%s" % log)

    @xdb_create_task(task_name='start xdb containers')
    def _start_xdb_container(self):
        for node in self.nodes:
            volumes = self._generate_xdb_volumes(node)
            self._create_volume_dirs_if_needed(volumes)
            self._write_pod_info(node)
            ports = self._generate_xdb_export_ports(node)
            command = self._generate_xdb_container_command()
            mem_limit = self._generate_xdb_node_mem_limit(node)
            env = self._generate_xdb_env(node)
            client = DockerManager.get_client(node.host)
            if Config.instance().host_network_support():
                container = client.containers.run(self.engine_image, command, volumes=volumes, detach=True,
                                                  entrypoint='',
                                                  privileged=True,
                                                  environment=env, working_dir='/', name=node.name,
                                                  network_mode='host',
                                                  mem_limit=mem_limit,
                                                  cpuset_cpus=node.cpusets,
                                                  cpuset_mems=node.memsets,
                                                  memswap_limit=-1
                                                  )
            else:
                container = client.containers.run(self.engine_image, command, volumes=volumes, detach=True,
                                                  entrypoint='',
                                                  privileged=True,
                                                  environment=env, working_dir='/', name=node.name,
                                                  ports=ports,
                                                  mem_limit=mem_limit,
                                                  cpuset_cpus=node.cpusets,
                                                  cpuset_mems=node.memsets,
                                                  memswap_limit=-1
                                                  )
            node.container_id = container.short_id
            dbapi.update_container(self.name, container,
                                   host=node.host, role=self.xdb_type + '-engine',
                                   volumes=json.dumps(volumes), ports=json.dumps(ports), envs=json.dumps(env))

    def _generate_xdb_volumes(self, node):
        local_tools_dir = f'{pxd_working_dir}/data/cache/xcluster-tools'
        node_id = node.host.replace('.', '_') + '_' + str(node.mysql_port)
        data_dir = f'{pxd_working_dir}/data/polarx/{node_id}'
        shared_channel_file = f'{pxd_working_dir}/data/shared/{self.name}'
        template_dir = f'{pxd_working_dir}/data/template'
        # this is for k8s environment
        podinfo_dir = f'{pxd_working_dir}/data/podinfo/{node_id}'
        mysqllog_dir = f'{pxd_working_dir}/data/polarx-log/{node_id}'

        return {
            local_tools_dir: {'bind': '/xcluster-tools', 'mode': 'ro'},
            local_tools_dir: {'bind': '/tools/xstore', 'mode': 'ro'},
            data_dir: {'bind': '/data/mysql', 'mode': 'rw'},
            shared_channel_file: {'bind': '/data/shared', 'mode': 'ro'},
            template_dir: {'bind': '/data/template', 'mode': 'ro'},
            podinfo_dir: {'bind': '/etc/podinfo', 'mode': 'ro'},
            mysqllog_dir: {'bind': '/data/mysql-log', 'mode': 'rw'}
        }

    def _create_volume_dirs_if_needed(self, volumes):
        for host in self.hosts:
            FileManager.mkdirs(host, volumes.keys())

    def _generate_xdb_node_mem_limit(self, node):
        if node.role == 'Logger':
            return min(int(self.mem_limit), constant.LOGGER_MAX_MEM)
        return self.mem_limit

    def _generate_xdb_ports(self, node):
        ports = {str(node.mysql_port) + '/tcp': node.mysql_port,
                 str(node.paxos_port) + '/tcp': node.paxos_port,
                 str(node.polarx_port) + '/tcp': node.polarx_port}
        return ports

    def _generate_xdb_export_ports(self, node):
        return {
            str(node.mysql_port) + '/tcp': node.mysql_port,
        }

    def _generate_xdb_container_command(self):
        return 'bash -c "/tools/xstore/current/venv/bin/python3 /tools/xstore/current/entrypoint.py"'

    def _generate_engine_home(self):
        if self.engine_type == 'galaxy':
            return '/opt/galaxy_engine'
        elif self.engine_type == 'xcluster':
            if self.engine_version == '8.0':
                return '/u01/xcluster80_current'
            elif self.engine_version == '5.7':
                return '/u01/xcluster_current'
        logger.info("no engine and version found, return galaxy engine default")
        return '/opt/galaxy_engine'

    def _generate_xdb_env(self, node):
        engine_home = self._generate_engine_home()
        env = [
            'ENGINE=' + self.engine_type,
            'ENGINE_HOME=' + engine_home,
            'LANG=en_US.utf8',
            'LC_ALL=en_US.utf8',
            'NODE_ROLE=' + node.container_role,
            'NODE_IP=' + node.host,
            'NODE_NAME=' + node.name,
            'POD_NAME=' + node.name,
            'POD_IP=' + node.host,
            'PORT_MYSQL=' + str(node.mysql_port),
            'PORT_PAXOS=' + str(node.paxos_port),
            'PORT_POLARX=' + str(node.polarx_port),
            'RPC_PROTOCOL_VERSION=' + Config.instance().rpc_protocol_version(),
            # Old envs
            'VOLUME_DATA=/data/mysql',
            'VOLUME_LOG=/data/mysql-log',
            'VOLUME_TEMPLATE=/data/template',
            'VOLUME_CONFIG=/data/template',
            'LOG_DATA_SEPARATION=true',
            'XCLUSTER_ID=1',
            'ROLE_POD=' + node.container_role,
            'VIRTUAL_ENV=/tools/xstore/current/venv',
            'XCLUSTER_VERSION=5.7',
            'LIMITS_CPU=' + str(self.cpu_limit * 1000),
            'LIMITS_MEM=' + str(self._generate_xdb_node_mem_limit(node))
        ]

        return env

    @retry(stop_max_attempt_number=120, wait_fixed=5000, retry_on_result=retry_if_result_none)
    def _wait_leader_elected(self):
        for node in self.nodes:
            client = DockerManager.get_client(node.host)
            container = client.containers.get(node.container_id)

            (exit_code, output) = container.exec_run(cmd=["/tools/xstore/current/venv/bin/python3",
                                                          "/tools/xstore/current/cli.py", "consensus", "role"])
            output = output.decode('utf-8').strip()

            # Not support x-paxos
            if "PROCEDURE dbms_consensus.show_cluster_local does not exist" in output:
                (exit_code, output) = container.exec_run(cmd=["/tools/xstore/current/venv/bin/python3",
                                                              "/tools/xstore/current/cli.py", "ping"])
                logger.info(exit_code)
                if exit_code == 0:
                    self.leader_node = node
                    return node
                else:
                    return None

            if exit_code != 0:
                continue

            lines = output.split("\n")
            role = lines[0]
            if len(lines) > 1:
                role = lines[-1]

            logger.info("consensus role: " + role)
            if role == constant.ROLE_LEADER:
                if self.leader_node is None \
                        or self.leader_node.container_id != node.container_id:
                    self.leader_node = node
                    self.leader_cnt = 1
                else:
                    self.leader_cnt += 1

        if self.leader_cnt >= 3:
            return self.leader_node
        else:
            return None

    @xdb_create_task(task_name='create account')
    def _create_admin_account(self):
        leader_node = self._wait_leader_elected()
        client = DockerManager.get_client(leader_node.host)
        container = client.containers.get(leader_node.container_id)
        admin_password = ''.join(secrets.choice(string.ascii_letters) for i in range(8))
        exit_code = self._run_create_account_cmd(container, admin_password)

        if exit_code != 0:
            logger.error("Failed to create admin account after retry for " + self.name)
            return Flow.FAIL

        self.user_name = "admin"
        self.password = admin_password
        return Flow.SUCCESS

    @retry(stop_max_attempt_number=3, wait_fixed=10000, retry_on_result=retry_if_result_none)
    def _run_create_account_cmd(self, container, admin_password):
        (exit_code, output) = container.exec_run(cmd=["/tools/xstore/current/venv/bin/python3",
                                                      "/tools/xstore/current/cli.py", "account",
                                                      "create", "-u", "admin",
                                                      "-p", admin_password])
        if exit_code != 0:
            logger.error("Create xdb account failed, output: " + output)
            return None

        output = output.decode('utf-8').strip()
        logger.debug("Create xdb account success, output: " + output)
        return exit_code

    def storage_type(self):
        logger.info("engine_type: " + self.engine_type)
        if self.engine_type == constant.XCLUSTER_ENGINE:
            if self.engine_version == "5.7":
                return constant.STORAGE_TYPE_XCLUSTER
            elif self.engine_version == "8.0":
                return constant.STORAGE_TYPE_RDS80_XCLUSTER
            else:
                raise ValueError('Not supported data node engine')
        elif self.engine_type == constant.GALAXY_ENGINE:
            if self.leader_only:
                return constant.STORAGE_TYPE_GALAXY_SINGLE
            else:
                return constant.STORAGE_TYPE_GALAXY_PAXOS
        else:
            raise ValueError('Not supported data node engine')

@retry(stop_max_attempt_number=2, wait_fixed=5000, retry_on_result=retry_if_result_none)
def query_container_role(host, container_name, container_id):
    client = DockerManager.get_client(host)
    try:
        container = client.containers.get(container_id)

        if container.status == 'exit':
            logger.info("node:%s, container: %s is not running" % (host, container_name))
            return None

        (exit_code, output) = container.exec_run(cmd=["/tools/xstore/current/venv/bin/python3",
                                                      "/tools/xstore/current/cli.py", "consensus", "role"])

        output = output.decode('utf-8').strip()
        logger.info("host: %s, container: %s output: %s" % (host, container_name, output))

        if exit_code != 0:
            logger.info("host: %s, container_id: %s, exit code: %s"(host, container_name, str(exit_code)))
            None

        lines = output.split("\n")
        for line in lines:
            if line in constant.ROLE_LIST:
                return line

        return "unknown"
    except Exception as ex:
        logger.info("failed to check node role, node:%s, host:%s, ex: %s" % (container_name, host, str(ex)))
        client.close()
        return None
    finally:
        client.close()


def change_leader_container(cur_leader_host, cur_leader_container_id, cur_leader_container_name,
                            expect_leader_container_name):
    client = DockerManager.get_client(cur_leader_host)
    container = client.containers.get(cur_leader_container_id)
    try:
        (exit_code, output) = container.exec_run(cmd=["/tools/xstore/current/venv/bin/python3",
                                                      "/tools/xstore/current/cli.py", "consensus", "change-leader",
                                                      expect_leader_container_name])
        logger.info("change leader output: %s" % output)
        return True
    except Exception as ex:
        logger.info("change leader failed, current leader: %s, expect leader: %s" % (cur_leader_container_name,
                                                                                     expect_leader_container_name))
        return False
    finally:
        client.close()


class XdbNode:

    def __init__(self, host, mysql_port, paxos_port, polarx_port, role, cpusets=None, memsets=None):
        self.host = host
        self.mysql_port = mysql_port
        self.paxos_port = paxos_port
        self.polarx_port = polarx_port
        self.role = role
        self.container_ip = None
        self.container_id = None
        self.name = None
        self.container_role = _generate_container_role(role)
        self.cpusets = cpusets
        self.memsets = memsets
