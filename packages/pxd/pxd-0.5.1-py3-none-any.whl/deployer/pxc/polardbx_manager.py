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

import configparser

import click
import yaml

from deployer._repo import repo_dir
from deployer.config.config import Config
from deployer.pxc.polardbx_cluster import PolarDBXCluster
from deployer.sqlite.sqlite_manager import SQLiteManager


def create_tryout_pxc(name, cn_replica, cn_version, dn_replica, dn_version, cdc_replica, cdc_version, leader_only=True):
    click.echo("Start creating PolarDB-X cluster %s on your local machine" % name)
    click.echo("PolarDB-X Cluster params:")
    click.echo(" * cn count: %d, version: %s" % (cn_replica, cn_version))
    click.echo(" * dn count: %d, version: %s" % (dn_replica, dn_version))
    click.echo(" * cdc count: %d, version: %s" % (cdc_replica, cdc_version))
    click.echo(" * gms count: %d, version: %s" % (1, dn_version))
    click.echo(" * leader_only: %r" % leader_only)
    pxc = PolarDBXCluster(name, cn_replica, cn_version, dn_replica, dn_version, cdc_replica, cdc_version,
                          leader_only=leader_only)
    pxc.create()


def list_all_pxc():
    rows = SQLiteManager.execute_query("select pxc_name, cn_replica, dn_replica, cdc_replica, pxc_status "
                                       "from polardbx_cluster")
    """
    click header first
    """
    click.echo(f"{'NAME' : <30}{'CN' : <10}{'DN' : <10}{'CDC' : <10}{'STATUS' : <15}")
    pxc_list = []
    for row in rows:
        click.echo(f"{row['pxc_name'] : <30}{str(row['cn_replica']) : <10}{str(row['dn_replica']) : <10}"
                   f"{str(row['cdc_replica']) : <10}{row['pxc_status'] : <15}")
        pxc_list.append(row[0])
    return pxc_list


def delete_pxc(pxc_name):
    PolarDBXCluster.delete(pxc_name)


def check_pxc(pxc_name, type, repair):
    click.echo("Check pxc: %s, type: %s, repair: %s" % (pxc_name, type, str(repair)))
    if type not in ('cn', 'dn'):
        click.echo("check type: %s dose not support, only support cn or dn")
        return
    if type == 'dn':
        PolarDBXCluster.check_dn_leader(pxc_name, repair)
    elif type == 'cn':
        PolarDBXCluster.check_cn_alive(pxc_name, repair)


def cleanup_all_pxc():
    click.echo("Prepare to delete all PolarDB-X clusters")
    if click.confirm(click.style('All PolarDB-X clusters will be deleted, do you want to continue?', fg='blue'),
                     abort=True):
        rows = SQLiteManager.execute_query("select * from polardbx_cluster")
        for row in rows:
            pxc_name = row[3]
            PolarDBXCluster.delete(pxc_name)


def create_full_pxc(topology_yaml_file, cn_version, dn_version, cdc_version):
    if not topology_yaml_file:
        click.echo("Please specify topology file")
        return
    click.echo("yaml file: %s" % topology_yaml_file)
    with open(topology_yaml_file, 'r') as stream:
        try:
            data = yaml.load(stream)
            pxc_name = data['cluster']['name']

            pxc = PolarDBXCluster(pxc_name, topology=data)
            pxc.create()
        except yaml.YAMLError as ex:
            click.echo("Please check yaml format, error: %s" % str(ex))


def print_pxd_version():
    Config.instance().load_config()
    version_file = repo_dir.joinpath("deployer/version.txt")
    config = configparser.RawConfigParser()
    config.read(version_file)
    click.echo('pxd version: ' + config.get('default', 'version'))
