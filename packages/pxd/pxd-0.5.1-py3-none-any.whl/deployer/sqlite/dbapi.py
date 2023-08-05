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
from deployer.sqlite.sqlite_manager import SQLiteManager


logger = logging.getLogger(__name__)


def update_xdb(xdb):
    try:
        sql = """replace into polardbx_xdb (
        'id', 'gmt_created', 'gmt_modified', 'xdb_name', 'xdb_status', 
        'xdb_type','pxc_name', 'version', 'leader_only', 'leader_container_name', 
        'root_account', 'root_password', 'details')
         values (NULL, date('now'), date('now'), :xdb_name, :status, 
         :xdb_type, :pxc_name, :version, :leader_only, :leader_container,
         :username, :password, :err)
        """
        SQLiteManager.execute_update(sql, {
            'xdb_name': xdb.name,
            'status': xdb.status,
            'xdb_type': xdb.xdb_type,
            'pxc_name': xdb.pxc_name,
            'version': str(xdb.version),
            'leader_only': xdb.leader_only,
            'leader_container': str(xdb.leader_node.name if xdb.leader_node is not None else None),
            'username': str(xdb.user_name),
            'password': str(xdb.password),
            'err': str(xdb.error)
        })
    except Exception as ex:
        logger.error("failed to update polardbx xdb record", ex)


def update_pxc(pxc):
    try:
        sql = """replace into polardbx_cluster (
        'id', 'gmt_created', 'gmt_modified', 'pxc_name', 'pxc_status', 
        'cn_replica', 'cn_version', 'dn_replica', 'dn_version', 'leader_only', 
        'cdc_replica', 'cdc_version', 'root_account', 'root_password', 'details') values (
        NULL, date('now'), date('now'), :pxc_name, :pxc_status,
        :cn_replica, :cn_version, :dn_replica, :dn_version, :leader_only,
        :cdc_replica, :cdc_version, :root_account, :root_password, :details)
        """
        SQLiteManager.execute_update(sql, {
            'pxc_name': pxc.pxc_name,
            'pxc_status': pxc.pxc_status,
            'cn_replica': pxc.cn_replica,
            'cn_version': str(pxc.cn_version),
            'dn_replica': pxc.dn_replica,
            'dn_version': str(pxc.dn_version),
            'leader_only': pxc.leader_only,
            'cdc_replica': pxc.cdc_replica,
            'cdc_version': str(pxc.cdc_version),
            'root_account': str(pxc.root_account),
            'root_password': str(pxc.root_password),
            'details': str(pxc.error)
        })
    except Exception as ex:
        logger.error("failed to update polardbx record", ex)


def update_container(resource_name, container, **kwargs):
    try:
        sql = """replace into container(
        'id', 'gmt_created', 'gmt_modified', 'container_name','container_id', 
        'host', 'container_ip', 'container_type', 'resource_name', 
        'local_volumes', 'ports', 'env') values (
        NULL, date('now'), date('now'), :container_name, :container_id, 
        :host, :container_ip, :container_type, :resource_name,
        :local_volumes, :ports, :envs)
        """
        SQLiteManager.execute_update(sql, {
            'container_name': container.name,
            'container_id': container.short_id,
            'host': kwargs['host'],
            'container_ip': container.attrs['NetworkSettings']['IPAddress'],
            'container_type': kwargs['role'],
            'resource_name': resource_name,
            'local_volumes': kwargs['volumes'],
            'ports': kwargs['ports'],
            'envs': kwargs['envs']
        })
    except Exception as ex:
        logger.error("failed to update polardbx container record", ex)


def list_containers_by_pxc(pxc_name):
    sql = """select * from container where resource_name=:resource_name
    """
    containers = SQLiteManager.execute_query(sql, {
        'resource_name': pxc_name
    })
    return containers

def list_cn_containers_by_pxc(pxc_name):
    sql = """select * from container where container_type = 'cn-engine' and resource_name=:resource_name
    """
    containers = SQLiteManager.execute_query(sql, {
        'resource_name': pxc_name
    })
    return containers


def list_xdbs_by_pxc(pxc_name):
    sql = """select * from polardbx_xdb where pxc_name=:pxc_name
    """
    xdbs = SQLiteManager.execute_query(sql, {
        'pxc_name': pxc_name
    })
    return xdbs


def list_xdb_containers_by_names(xdb_names):
    sql = f"select * from container where resource_name in ({','.join(xdb_names)})"
    containers = SQLiteManager.execute_query(sql)
    return containers

def list_xdb_containers_by_name(xdb_name):
    sql = f"select * from container where resource_name=:xdb_name"
    containers = SQLiteManager.execute_query(sql, {
        'xdb_name': xdb_name
    })
    return containers


def get_pxc_by_name(pxc_name):
    return SQLiteManager.execute_query(f"select * from polardbx_cluster where pxc_name = '{pxc_name}'")


def delete_pxc_related_records(pxc_name):
    delete_sqls = []

    xdbs = list_xdbs_by_pxc(pxc_name)
    for xdb in xdbs:
        delete_sqls.append(f"delete from container where resource_name='{xdb['xdb_name']}'")
        delete_sqls.append(f"delete from polardbx_xdb where xdb_name='{xdb['xdb_name']}'")

    delete_sqls.extend([
        f"delete from container where resource_name = '{pxc_name}'",
        f"delete from polardbx_cluster where pxc_name = '{pxc_name}'"])

    SQLiteManager.execute_script(";".join(delete_sqls))

