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
import sqlite3

from deployer._repo import pxd_working_dir

logger = logging.getLogger(__name__)

class SQLiteManager:

    db_file = pxd_working_dir + "/polardbx.db"

    def __init__(self):
        pass

    @staticmethod
    def execute_update(sql):
        logger.info("prepare to execute sql for sql lite: %s, sql: %s", SQLiteManager.db_file, sql)
        try:
            with sqlite3.connect(SQLiteManager.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute(sql)
                conn.commit()
        except Exception as e:
            logger.error("execute update for xdb failed, xdb: %s, sql: %s", SQLiteManager.db_file, sql, e)

    @staticmethod
    def execute_script(sql_script):
        logger.info("prepare to execute sql for sql lite: %s, sql script: %s", SQLiteManager.db_file, sql_script)
        try:
            with sqlite3.connect(SQLiteManager.db_file) as conn:
                cursor = conn.cursor()
                cursor.executescript(sql_script)
                conn.commit()
        except Exception as e:
            logger.error("execute update for xdb failed, xdb: %s, sql: %s", SQLiteManager.db_file, sql_script, e)

    @staticmethod
    def execute_query(sql):
        logger.info("prepare to execute sql for sql lite: %s, sql script: %s", SQLiteManager.db_file, sql)
        try:
            with sqlite3.connect(SQLiteManager.db_file) as conn:
                cursor = conn.cursor()
                result = []
                for row in cursor.execute(sql):
                    result.append(row)
                return result
        except Exception as e:
            logger.error("execute update for xdb failed, xdb: %s, sql: %s", SQLiteManager.db_file, sql, e)

