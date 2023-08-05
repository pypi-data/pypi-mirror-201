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

import logging

import pymysql.cursors
from pymysql.constants import CLIENT

logger = logging.getLogger(__name__)

class MySQLManager:

    def __init__(self):
        pass

    @staticmethod
    def execute_update(xdb, sql_list=[], db='polardbx_meta_db'):
        leader = xdb.leader_node
        logger.info("prepare to execute sql for xdb: %s, sql list: %s", xdb, sql_list)
        try:
            with pymysql.connect(host=leader.host, port=leader.mysql_port, database=db,
                                 user=xdb.user_name, password=xdb.password,
                                 cursorclass=pymysql.cursors.DictCursor,
                                 client_flag=CLIENT.MULTI_STATEMENTS) as conn:
                with conn.cursor() as cursor:
                    for sql in sql_list:
                        if sql != '':
                            cursor.execute(sql)
                conn.commit()
        except Exception as e:
            logger.error("execute update for xdb failed, xdb: %s, sql: %s", xdb, sql_list, e)

    @staticmethod
    def execute_cn_sql(cn, password, sql='', db=''):
        with pymysql.connect(host=cn.host, port=cn.mysql_port,
                             user='polardbx_root', password=password,
                             cursorclass=pymysql.cursors.DictCursor,
                             client_flag=CLIENT.MULTI_STATEMENTS) as conn:
            with conn.cursor() as cursor:
                if sql:
                    cursor.execute(sql)