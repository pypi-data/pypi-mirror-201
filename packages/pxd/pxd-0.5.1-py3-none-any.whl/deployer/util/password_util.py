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

import base64
import secrets
import string

from Cryptodome.Cipher import AES


class PasswordUtil:

    def encrypt(self, key, data):
        mode = AES.MODE_ECB
        padding = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
        cryptos = AES.new(key.encode('utf-8'), mode)
        cipher_text = cryptos.encrypt(padding(data).encode("utf-8"))
        return base64.b64encode(cipher_text).decode("utf-8")

    def decrypt(self, key, data):
        cryptos = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        decrpytBytes = base64.b64decode(data)
        meg = cryptos.decrypt(decrpytBytes).decode('utf-8')
        return meg[:-ord(meg[-1])]


if __name__ == '__main__':
    print(PasswordUtil().decrypt("HQlIoYbRinjMlsAZ", "0D9yHgkENcFF3wrLdRneDw=="))


def random_str(count):
    return ''.join(secrets.choice(string.ascii_letters) for _ in range(count))