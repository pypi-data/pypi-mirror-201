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

import functools
import logging

import click

import deployer.sqlite.dbapi as dbapi

logger = logging.getLogger(__name__)


def pxc_create_task(task_name="DEFAULT"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            pxc = args[0]
            try:
                logger.info('task_name: %s, call %s():', task_name, func.__name__)
                click.echo('    ' + task_name)
                ret = func(*args, **kw)
                dbapi.update_pxc(pxc)
                return ret
            except Exception as ex:
                pxc.pxc_status = "failed"
                pxc.error = ex
                dbapi.update_pxc(pxc)
                raise ex

        return wrapper

    return decorator


def xdb_create_task(task_name="DEFAULT"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            xdb = args[0]
            try:
                logger.info('task_name: %s, call %s():', task_name, func.__name__)
                ret = func(*args, **kw)
                dbapi.update_xdb(xdb)
                return ret
            except Exception as ex:
                xdb.status = 'fail'
                xdb.error = ex
                dbapi.update_xdb(xdb)
                raise ex

        return wrapper

    return decorator


def download_task(task_name="DEFAULT"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            click.echo('    ' + task_name)
            func(*args, **kw)

        return wrapper
    return decorator
