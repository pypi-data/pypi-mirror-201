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

import configparser
import os
import platform
import re
import sys

from deployer._repo import pxd_working_dir
from deployer.config.log_config import setup_logging
from deployer.config.metadb_config import setup_metadb


class Config:
    _instance = None

    DOCKER_REPO_URL = "polardbx/"

    CN_IMAGE_NAME = "polardbx-sql"
    DN_IMAGE_NAME = "polardbx-engine"
    CDC_IMAGE_NAME = "polardbx-cdc"

    CN_IMAGE_VERSION = 'latest'
    DN_IMAGE_VERSION = "latest"
    CDC_IMAGE_VERSION = "latest"

    CN_TOOL_IMAGE_NAME = "polardbx-init"
    CN_TOOL_IMAGE_VERSION = 'latest'

    DN_TOOL_IMAGE_NAME = "xstore-tools"
    DN_TOOL_IMAGE_VERSION = "latest"

    DEBUG_MODE = False
    run_host = None

    SSH_PORT = 22
    PULL_LATEST_IMAGES = True
    RPCProtocolVersion = "2"
    MYCNF_TEMPLATE = ""
    DN_PASSWORD_KEY = ""

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        pass

    @staticmethod
    def instance():
        return Config()

    @classmethod
    def load_config(cls, **kwargs):
        pxd_config_file = pxd_working_dir + '/config'
        if os.path.exists(pxd_config_file):
            config = configparser.RawConfigParser()
            config.optionxform = lambda option: option
            config.read(pxd_config_file)
            for section_name, sections in config.items():
                for key, value in sections.items():
                    if hasattr(cls.instance(), key):
                        cls.instance().__setattr__(key, value)
        for key, value in kwargs.items():
            if value is not None:
                cls.instance().__setattr__(key, value)

    @property
    def all_polardbx_images(self):
        return [
            self.cn_image,
            self.cn_tool_image,
            self.dn_image,
            self.dn_tool_image,
            self.cdc_image
        ]

    @property
    def cn_image(self):
        return f'{self.DOCKER_REPO_URL}{self.CN_IMAGE_NAME}:{self.CN_IMAGE_VERSION}'

    @property
    def cn_tool_image(self):
        return f'{self.DOCKER_REPO_URL}{self.CN_TOOL_IMAGE_NAME}:{self.CN_TOOL_IMAGE_VERSION}'

    @property
    def dn_image(self):
        return f'{self.DOCKER_REPO_URL}{self.DN_IMAGE_NAME}:{self.DN_IMAGE_VERSION}'

    @property
    def dn_tool_image(self):
        return f'{self.DOCKER_REPO_URL}{self.DN_TOOL_IMAGE_NAME}:{self.DN_TOOL_IMAGE_VERSION}'

    @property
    def cdc_image(self):
        return f'{self.DOCKER_REPO_URL}{self.CDC_IMAGE_NAME}:{self.CDC_IMAGE_VERSION}'

    @staticmethod
    def host_network_support():
        """
        Docker for mac is run on a virtual machine, so only 'bridge' mode is supported
        :return: Return false is platform is Darwin, otherwise return true.
        """
        if Config.instance().run_host == '127.0.0.1':
            return False
        if platform.system() in ("Darwin", "Windows"):
            return False
        return True

    @staticmethod
    def debug_mode_enabled():
        return Config.instance().DEBUG_MODE

    @staticmethod
    def ssh_port():
        return Config.instance().SSH_PORT

    @staticmethod
    def pull_latest_images():
        return Config.instance().PULL_LATEST_IMAGES

    @staticmethod
    def host_arch():
        """Returns the host architecture with a predictable string."""
        host_arch = platform.machine()

        # Convert machine type to format recognized by gyp.
        if re.match(r'i.86', host_arch) or host_arch == 'i86pc':
            host_arch = 'x86'
        elif host_arch in ['x86_64', 'amd64']:
            host_arch = 'x64'
        elif host_arch.startswith('arm'):
            host_arch = 'arm'
        elif host_arch.startswith('aarch64'):
            host_arch = 'arm64'
        elif host_arch.startswith('mips64'):
            host_arch = 'mips64'
        elif host_arch.startswith('mips'):
            host_arch = 'mips'
        elif host_arch.startswith('ppc'):
            host_arch = 'ppc'
        elif host_arch.startswith('s390'):
            host_arch = 's390'

        return host_arch

    @staticmethod
    def host_arm_arch():
        return "arm" in Config.host_arch()

    @staticmethod
    def rpc_protocol_version():
        return Config.instance().RPCProtocolVersion

    @staticmethod
    def dn_passwork_key():
        return Config.instance().DN_PASSWORD_KEY


def setup_pxd_context():
    setup_pxd_working_dir()
    setup_logging()
    setup_metadb()


def setup_pxd_working_dir():
    if os.path.exists(pxd_working_dir):
        return
    os.makedirs(pxd_working_dir, exist_ok=True)
