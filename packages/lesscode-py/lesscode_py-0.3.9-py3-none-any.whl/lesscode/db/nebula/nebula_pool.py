# -*- coding: utf-8 -*-
# author:chao.yy
# email:yuyc@ishangqi.com
# date:2022/2/17 2:45 下午
# Copyright (C) 2022 The lesscode Team
import ssl

from nebula3.gclient.net import ConnectionPool
from nebula3.Config import Config, SSL_config

from lesscode.db.base_connection_pool import BaseConnectionPool


class NebulaPool(BaseConnectionPool):
    """
    mysql 数据库链接创建类
    """

    async def create_pool(self):
        pass

    def sync_create_pool(self):
        config = Config()
        ssl_conf = None
        config.max_connection_pool_size = self.conn_info.max_size
        config.min_connection_pool_size = self.conn_info.min_size
        if self.conn_info.params and isinstance(self.conn_info.params, dict):
            config.timeout = self.conn_info.params.get("timeout", 0)
            config.idle_time = self.conn_info.params.get("idle_time", 0)
            config.interval_check = self.conn_info.params.get("interval_check", -1)
            ssl_config = self.conn_info.params.get("ssl_conf", {})
            if ssl_conf and isinstance(ssl_conf, dict):
                ssl_conf = SSL_config()
                ssl_conf.unix_socket = ssl_config.get("unix_socket", None)
                ssl_conf.ssl_version = ssl_config.get("ssl_version", None)
                ssl_conf.cert_reqs = ssl_config.get("cert_reqs", ssl.CERT_NONE)
                ssl_conf.ca_certs = ssl_config.get("ca_certs", None)
                ssl_conf.verify_name = ssl_config.get("verify_name", None)
                ssl_conf.keyfile = ssl_config.get("keyfile", None)
                ssl_conf.certfile = ssl_config.get("certfile", None)
                ssl_conf.allow_weak_ssl_versions = ssl_config.get("allow_weak_ssl_versions", None)
        pool = ConnectionPool()
        pool.init([(self.conn_info.host, self.conn_info.port)], config, ssl_conf)
        return pool
