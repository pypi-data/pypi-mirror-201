/*
 *  Copyright [2013-2021], Alibaba Group Holding Limited
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */

CREATE TABLE IF NOT EXISTS polardbx_cluster (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  gmt_created DATE NOT NULL,
  gmt_modified DATE NOT NULL,
  pxc_name VARCHAR(128) UNIQUE NOT NULL,
  pxc_status VARCHAR(64) NOT NULL,
  cn_replica INT NOT NULL,
  cn_version varchar(1024) NOT NULL,
  dn_replica INT NOT NULL,
  dn_version varchar(1024) NOT NULL,
  cdc_replica INT NOT NULL DEFAULT '0',
  cdc_version varchar(1024) NOT NULL DEFAULT 'latest',
  leader_only TINYINT NOT NULL,
  root_account varchar(128) NOT NULL,
  root_password varchar(128) NOT NULL,
  details text
);

CREATE TABLE IF NOT EXISTS polardbx_xdb (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  gmt_created DATE NOT NULL,
  gmt_modified DATE NOT NULL,
  xdb_name VARCHAR(128) UNIQUE NOT NULL,
  xdb_type varchar(64) NOT NULL,
  xdb_status VARCHAR(64) NOT NULL,
  pxc_name VARCHAR(128) NOT NULL,
  version varchar(1024) NOT NULL,
  leader_only tint NOT NULL,
  leader_container_name VARCHAR(128) NOT NULL,
  root_account varchar(128) NOT NULL,
  root_password varchar(128) NOT NULL,
  details text
);

CREATE TABLE IF NOT EXISTS container (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  gmt_created DATE NOT NULL,
  gmt_modified DATE NOT NULL,
  container_name VARCHAR(128) UNIQUE NOT NULL,
  container_id VARCHAR(128) NOT NULL,
  host varchar(64) NOT NULL,
  container_ip varchar(64) NOT NULL,
  container_type varchar(64) NOT NULL,
  resource_name VARCHAR(128) NOT NULL,
  local_volumes text NOT NULL,
  ports text NOT NULL,
  env text NOT NULL
);