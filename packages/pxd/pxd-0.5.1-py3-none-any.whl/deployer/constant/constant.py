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

STATUS_CREATING = 'Creating'
STATUS_RUNNING = 'Running'

ROLE_LEADER = 'leader'
ROLE_FOLLOWER = 'follower'
ROLE_LOGGER = 'logger'

ROLE_LIST = [ROLE_LEADER, ROLE_FOLLOWER, ROLE_LOGGER]

PXC_ROOT_ACCOUNT = 'polardbx_root'

STORAGE_KIND_DN = 0
STORAGE_KIND_GMS = 2

STORAGE_TYPE_GALAXY_LEADER_ONLY = 4
STORAGE_TYPE_GALAXY_PAXOS = 3
STORAGE_TYPE_XCLUSTER = 0
STORAGE_TYPE_XCLUSTER_LEADER_ONLY = 1
STORAGE_TYPE_RDS80_XCLUSTER = 3
STORAGE_TYPE_GALAXY_CLUSTER = 5
STORAGE_TYPE_GALAXY_SINGLE = 4

XCLUSTER_ENGINE = 'xcluster'
GALAXY_ENGINE = 'galaxy'

LOGGER_MAX_MEM = 4294967296
