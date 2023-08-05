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

import hashlib


class PxcUser:

    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password
        self.host = '%'
        self.enc_password = hashlib.sha1(password.encode('utf-8')).hexdigest()
        self.select_priv = 1
        self.insert_priv = 1
        self.update_priv = 1
        self.delete_priv = 1
        self.create_priv = 1
        self.drop_priv = 1
        self.grant_priv = 1
        self.index_priv = 1
        self.alter_priv = 1
        self.show_view_priv = 1
        self.create_view_priv = 1
        self.create_user_priv = 1
        self.meta_db_priv = 1
