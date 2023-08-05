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

import docker

from deployer.config.config import Config

client_cache = {}


def get_client(host=None, port=2375):
    """
    Create docker client according to host, including local machine and remote server
    :param host:
    :param port:
    :return: docker client
    """
    if host is None:
        host = '127.0.0.1'

    client = client_cache.get(host)
    if client is not None:
        return client

    if host == '127.0.0.1':
        client = docker.from_env()
        client_cache[host] = client
        return client
    else:
        docker_url = "ssh://%s:%d" % (host, Config.ssh_port())
        client = docker.DockerClient(base_url=docker_url, timeout=60, max_pool_size=100)
        client_cache[host] = client
        return client
