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

from Cryptodome.Cipher import AES


class YamlUtil:

    def generateHostGroup(self):

        nodes = ["10.176.4.222", "10.176.4.223","10.176.4.224","10.176.5.222","10.176.5.224",
               "10.176.5.225","10.176.5.226","10.176.5.227","10.176.5.228",
               "10.176.5.229"]

        #nodes = ["10.133.3.240", "10.133.2.252", "10.133.2.253"]

        i = 0
        node_count = len(nodes)
        while i < node_count:
            print("- host_group: [%s, %s, %s]" % (nodes[i % node_count], nodes[(i + 1) % node_count],
                  nodes[(i + 2) % node_count]))
            print("- host_group: [%s, %s, %s]" % (nodes[i % node_count], nodes[(i + 1) % node_count],
                                                  nodes[(i + 2) % node_count]))
            print("- host_group: [%s, %s, %s]" % (nodes[i % node_count], nodes[(i + 1) % node_count],
                                                  nodes[(i + 2) % node_count]))
            print("- host_group: [%s, %s, %s]" % (nodes[i % node_count], nodes[(i + 1) % node_count],
                                                  nodes[(i + 2) % node_count]))
            print("- host_group: [%s, %s, %s]" % (nodes[i % node_count], nodes[(i + 1) % node_count],
                                                  nodes[(i + 2) % node_count]))
            i = i+1


    def generateCNHost(self):
        nodes = ["10.176.4.222", "10.176.4.223","10.176.4.224","10.176.5.222","10.176.5.224",
            "10.176.5.225","10.176.5.226","10.176.5.227","10.176.5.228",
            "10.176.5.229"]
        i = 0
        node_count = len(nodes)
        while i < node_count:
            print("- host: %s" % (nodes[i]))
            print("- host: %s" % (nodes[i]))
            print("- host: %s" % (nodes[i]))
            i = i + 1

if __name__ == '__main__':
    YamlUtil().generateHostGroup()
    #YamlUtil().generateCNHost()
    #print("ChannelException(2, 'Connect failed')')".encode())