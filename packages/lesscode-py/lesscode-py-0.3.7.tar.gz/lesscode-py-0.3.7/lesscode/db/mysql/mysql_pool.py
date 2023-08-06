# -*- coding: utf-8 -*-
# author:chao.yy
# email:yuyc@ishangqi.com
# date:2022/2/17 2:45 下午
# Copyright (C) 2022 The lesscode Team
import asyncio

import pymysql
from dbutils.persistent_db import PersistentDB
from dbutils.pooled_db import PooledDB

from lesscode.db.base_connection_pool import BaseConnectionPool
import aiomysql


class MysqlPool(BaseConnectionPool):
    """
    mysql 数据库链接创建类
    """

    async def create_pool(self):
        """
        创建mysql 异步连接池
        :return:
        """
        if self.conn_info.async_enable:
            pool = await aiomysql.create_pool(host=self.conn_info.host, port=self.conn_info.port,
                                              user=self.conn_info.user,
                                              password=self.conn_info.password,
                                              pool_recycle=self.conn_info.params.get("pool_recycle", 3600)
                                              if self.conn_info.params else 3600,
                                              db=self.conn_info.db_name, autocommit=True,
                                              minsize=self.conn_info.min_size,
                                              maxsize=self.conn_info.max_size)
            return pool
        else:
            raise NotImplementedError

    def sync_create_pool(self):
        pool = PooledDB(creator=pymysql, host=self.conn_info.host, port=self.conn_info.port, user=self.conn_info.user,
                        passwd=self.conn_info.password, db=self.conn_info.db_name,
                        mincached=self.conn_info.min_size, blocking=True, maxusage=self.conn_info.min_size,
                        maxshared=self.conn_info.max_size, maxcached=self.conn_info.max_size,
                        ping=1, maxconnections=self.conn_info.max_size, charset="utf8mb4", autocommit=True,
                        read_timeout=30)
        return pool
