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

from deployer.config.config import setup_pxd_context, Config
from deployer.download.polardbx_download import download_polardbx_packages
from deployer.pxc.polardbx_manager import create_tryout_pxc, list_all_pxc, delete_pxc, cleanup_all_pxc, create_full_pxc, \
    print_pxd_version, check_pxc

import warnings

warnings.filterwarnings("ignore")

@click.group()
def main():
    pass


@click.command(help='Create a minimum PolarDB-X cluster on local machine for tryout.')
@click.option("-name", default="pxc-tryout", help="PolarDB-X Cluster name, default: pxc-tryout")
@click.option("-cn_replica", default=1, help='cn node count')
@click.option("-cn_version", default="latest", help='cn node version')
@click.option("-dn_replica", default=1, help='dn node count')
@click.option("-dn_version", default="latest", help='dn node version')
@click.option("-cdc_replica", default=1, help='cdc node count')
@click.option("-cdc_version", default="latest", help='cdc node version')
@click.option("-repo", default="polardbx/", help="docker repo url, default is docker hub")
@click.option("-leader_only", default=True, help="create gms and dn with single node by default, otherwise a x-paxos "
                                                 "cluster")
@click.option("-debug", "-d", default=False, help='debug mode for troubleshooting')
@click.option("-ssh_port", default=22, help='debug mode for troubleshooting')
@click.option("-pull_latest_images", default=True, help='pull latest images, if false will use local image')
@click.option("-rpc_version", default="2", help='rpc protocol version for cn and dn')
def tryout(name, cn_replica, cn_version, dn_replica, dn_version, cdc_replica, cdc_version, repo, leader_only, debug,
           ssh_port, pull_latest_images, rpc_version):
    setup_pxd_context()
    Config.instance().load_config(CN_IMAGE_VERSION=cn_version, DN_IMAGE_VERSION=dn_version,
                                  CDC_IMAGE_VERSION=cdc_version, DOCKER_REPO_URL=repo,
                                  DEBUG_MODE=debug, SSH_PORT=ssh_port, PULL_LATEST_IMAGES=pull_latest_images,
                                  RPCProtocolVersion=rpc_version)
    create_tryout_pxc(name, cn_replica, cn_version, dn_replica, dn_version, cdc_replica, cdc_version, leader_only)


@click.command(help="Create a full PolarDB-X cluster on multi hosts.")
@click.option("-file", "-f", default=None, help='PolarDB-X cluster topology yaml file')
@click.option("-cn_version", default="latest", help='cn node version')
@click.option("-dn_version", default="latest", help='dn node version')
@click.option("-cdc_version", default="latest", help='cdc node version')
@click.option("-repo", default="polardbx/", help="docker repo url, default is docker hub")
@click.option("-debug", "-d", default=False, help='debug mode for troubleshooting')
@click.option("-ssh_port", default=22, help='ssh port')
@click.option("-pull_latest_images", default=True, help='pull latest images, if false will use local image')
@click.option("-mycnf_template", default="", help='my.cnf template file')
@click.option("-rpc_version", default="2", help='rpc protocol version for cn and dn')
@click.option("-cn_tool_image_version", default="latest", help='polardbx-init image tag')
@click.option("-dn_tool_image_version", default="latest", help='xstore-tools image tag')
@click.option("-dn_password_key", default="", help='dn password key')
def create(file, cn_version, dn_version, cdc_version, repo, debug, ssh_port, pull_latest_images, mycnf_template,
           rpc_version, cn_tool_image_version, dn_tool_image_version, dn_password_key):
    setup_pxd_context()
    Config.instance().load_config(CN_IMAGE_VERSION=cn_version, DN_IMAGE_VERSION=dn_version,
                                  CDC_IMAGE_VERSION=cdc_version, DOCKER_REPO_URL=repo,
                                  DEBUG_MODE=debug, SSH_PORT=ssh_port,
                                  PULL_LATEST_IMAGES=pull_latest_images,
                                  MYCNF_TEMPLATE=mycnf_template, RPCProtocolVersion=rpc_version,
                                  CN_TOOL_IMAGE_VERSION=cn_tool_image_version,
                                  DN_TOOL_IMAGE_VERSION=dn_tool_image_version,
                                  DN_PASSWORD_KEY=dn_password_key)

    create_full_pxc(file, cn_version, dn_version, cdc_version)


@click.command(help="List PolarDB-X clusters.")
def list():
    setup_pxd_context()
    list_all_pxc()


@click.command(help="Clean up all PolarDB-X clusters.")
def cleanup():
    setup_pxd_context()
    cleanup_all_pxc()


@click.command(help="Delete specific PolarDB-X cluster.")
@click.option("-ssh_port", default=22, help='debug mode for troubleshooting')
@click.argument("name", default=None)
def delete(name, ssh_port):
    setup_pxd_context()
    Config.instance().load_config(SSH_PORT=ssh_port)
    delete_pxc(name)


@click.command(help="Print pxd version.")
def version():
    print_pxd_version()


@click.command(help="Check dn leader.")
@click.argument("name", default=None)
@click.option("-t", "--type", default=None, help='check cn or dn, values: [cn, dn]')
@click.option("-r", "--repair", default=False, help='set dn leader to correct container')
def check(name, type, repair):
    setup_pxd_context()
    check_pxc(name, type, repair)


@click.command(help="Download polardb-x offline install package for pxd or k8s")
@click.option("-e", "--env", default="pxd", help='download which env package, values: [pxd, k8s]')
@click.option("-a", "--arch", default="amd64", help='architecture for install package, values: [amd64, arm64]')
@click.option("-r", "--repo", default="", help="Target repo for download images, for example registry:5000")
@click.option("-i", "--image_list", default="", help="image list file, if specified, override the default images list")
@click.option("-d", "--dest", default="", help="dest directory for generated install packages")
def download(env, arch, repo, image_list, dest):
    download_polardbx_packages(env, arch, repo, image_list, dest)


main.add_command(tryout)
main.add_command(create)
main.add_command(list)
main.add_command(cleanup)
main.add_command(delete)
main.add_command(version)
main.add_command(check)
main.add_command(download)

if __name__ == '__main__':
    main()
