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

import os
import shutil

import spur
import spurplus

from deployer.config.config import Config


def _is_localhost(host):
    return host == '127.0.0.1' or host == 'localhost'


"""
This is a util class to handle file operation.
If host is local, directly access file, otherwise access remote file based on Paramiko
"""


class FileManager(object):

    shell_cache = {}

    def __init__(self):
        pass

    @staticmethod
    def mkdir(host, path, exist_ok=True):
        if _is_localhost(host):
            os.makedirs(path, exist_ok=exist_ok)
        else:
            shell = FileManager.get_shell(host)
            shell.mkdir(path, exist_ok=exist_ok, parents=True)

    @staticmethod
    def mkdirs(host, paths, exist_ok=True):
        if _is_localhost(host):
            for path in paths:
                os.makedirs(path, exist_ok=exist_ok)
        else:
            shell = FileManager.get_shell(host)
            for path in paths:
                shell.mkdir(path, exist_ok=exist_ok, parents=True)

    @staticmethod
    def exists(host, path):
        if _is_localhost(host):
            return os.path.exists(path)
        else:
            shell = FileManager.get_shell(host)
            return shell.exists(path)

    @staticmethod
    def remove(host, path):
        if _is_localhost(host):
            os.remove(path)
        else:
            shell = FileManager.get_shell(host)
            shell.remove(path)

    @staticmethod
    def rmdir(host, path):
        if _is_localhost(host):
            shutil.rmtree(path)
        else:
            shell = FileManager.get_shell(host)
            shell.remove(path, recursive=True)

    @staticmethod
    def copy(dst_host, src_file, dst_file):
        dst_dir = os.path.dirname(dst_file)
        if _is_localhost(dst_host):
            os.makedirs(dst_dir, exist_ok=True)
            shutil.copy(src_file, dst_file)
        else:
            shell = FileManager.get_shell(dst_host)
            shell.mkdir(dst_dir, exist_ok=True, parents=True)
            shell.put(
                local_path=src_file,
                remote_path=dst_file,
                create_directories=True,
                consistent=False)

    @staticmethod
    def write(host, file, content):
        file_dir = os.path.dirname(file)
        if _is_localhost(host):
            os.makedirs(file_dir, exist_ok=True)
            with open(file, 'w+') as f:
                f.write(content)
        else:
            shell = FileManager.get_shell(host)
            shell.mkdir(file_dir, exist_ok=True, parents=True)
            shell.write_text(file, text=content, consistent=False)

    @staticmethod
    def get_shell(host):
        if host not in FileManager.shell_cache:
            shell = spurplus.connect_with_retries(hostname=host, port=Config.ssh_port(), missing_host_key=spur.ssh.MissingHostKey.accept)
            FileManager.shell_cache[host] = shell
        return FileManager.shell_cache[host]
