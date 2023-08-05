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


class PxdContext:
    """
    Context for pxd command task, including tryout, install, upgrade
    """

    def __init__(self, pxc_name, cn_replica, cn_version, dn_replica, dn_version):
        self.pxc_name = pxc_name
        self.cn_replica = cn_replica
        self.cn_version = cn_version
        self.dn_replica = dn_replica
        self.dn_version = dn_version

