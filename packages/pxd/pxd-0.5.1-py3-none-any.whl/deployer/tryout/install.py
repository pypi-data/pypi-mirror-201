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

import click

from deployer.xdb.xdb import Xdb


def install_pxc_local(pxd_context):
    click.echo("prepare to install PolarDB-X Cluster")
    pre_check_install_env(pxd_context)
    start_dn_nodes(pxd_context)



def pre_check_install_env(pxd_context):
    # TODO
    pass

def start_dn_nodes(pxd_context):
    for i in range(pxd_context.dn_replica):
        xdb = Xdb(pxd_context.pxc_name + '-dn-' +str(i), pxd_context.dn_version)
        xdb.create()

def start_gms_nodes(pxd_context):
    gms = Xdb(pxd_context.pxc_name + '-gms', pxd_context.dn_version)
    gms.create()




