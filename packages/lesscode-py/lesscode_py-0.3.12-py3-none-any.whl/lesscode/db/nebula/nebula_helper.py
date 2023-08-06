# -*- coding: utf-8 -*-
# author:navysummer
# email:yuyc@ishangqi.com
# date:2021/11/26 3:56 下午
# Copyright (C) 2021 The lesscode Team
from functools import reduce

from nebula3.data.DataObject import Value, ValueWrapper, Relationship, PathWrapper, Node, Null
from nebula3.data.ResultSet import ResultSet
from nebula3.mclient import MetaCache, HostAddr
from nebula3.sclient.GraphStorageClient import GraphStorageClient
from tornado.options import options


class NebulaHelper:
    def __init__(self, pool):
        """
        初始化sql工具
        :param pool: 连接池名称
        """
        if isinstance(pool, str):
            self.pool, self.conn_info = options.database[pool]
        else:
            self.pool, self.conn_info = pool, None

    def exec_gql(self, sql, space=None):
        space = space if space else self.conn_info.db_name
        if not space:
            raise Exception(f"nebula no selection space")
        with self.pool.session_context(self.conn_info.user, self.conn_info.password) as session:
            session.execute(f'USE {space}')
            result = session.execute(sql)
        return result

    def fetch_data(self, sql, space=None):
        result = self.exec_gql(sql, space)
        result = convert(result)
        return result


class NebulaStorageHelper:
    def __init__(self, meta_cache_config: dict = None, storage_address_config: dict = None,
                 graph_storage_client_timeout=60000):
        self.meta_cache_config = meta_cache_config
        self.storage_address_config = storage_address_config
        self.graph_storage_client_timeout = graph_storage_client_timeout

    def get_meta_cache(self):
        meta_cache = None
        if self.meta_cache_config:
            meta_addrs = self.meta_cache_config.get("meta_addrs")
            timeout = self.meta_cache_config.get("timeout", 2000)
            load_period = self.meta_cache_config.get("load_period", 10)
            decode_type = self.meta_cache_config.get("decode_type", 'utf-8')
            meta_cache = MetaCache(meta_addrs, timeout, load_period, decode_type)
        return meta_cache

    def get_storage_addrs(self):
        storage_addrs = None
        storage_addrs = [HostAddr(host=sa.get("host"), port=sa.get("port")) for sa in storage_addrs]
        return storage_addrs

    def get_graph_storage_client(self):
        meta_cache = self.get_meta_cache()
        storage_addrs = self.get_storage_addrs()
        graph_storage_client = GraphStorageClient(meta_cache, storage_addrs, self.graph_storage_client_timeout)
        return graph_storage_client

    def scan_vertex(self, *args, **kwargs):
        graph_storage_client = self.get_graph_storage_client()
        resp = graph_storage_client.scan_vertex(*args, **kwargs)
        data = []
        while resp.has_next():
            result = resp.next()
            for vertex_data in result:
                data.append(vertex_data)
        return data

    def scan_edge(self, *args, **kwargs):
        graph_storage_client = self.get_graph_storage_client()
        resp = graph_storage_client.scan_edge(*args, **kwargs)
        data = []
        while resp.has_next():
            result = resp.next()
            for edge_data in result:
                data.append(edge_data)
        return data


cast_as = {
    Value.NVAL: "as_null",
    Value.__EMPTY__: "as_empty",
    Value.BVAL: "as_bool",
    Value.IVAL: "as_int",
    Value.FVAL: "as_double",
    Value.SVAL: "as_string",
    Value.LVAL: "as_list",
    Value.UVAL: "as_set",
    Value.MVAL: "as_map",
    Value.TVAL: "as_time",
    Value.DVAL: "as_date",
    Value.DTVAL: "as_datetime",
    Value.VVAL: "as_node",
    Value.EVAL: "as_relationship",
    Value.PVAL: "as_path",
    Value.GGVAL: "as_geography",
    Value.DUVAL: "as_duration"
}


def list_dict_duplicate_removal(data_list):
    run_function = lambda x, y: x if y in x else x + [y]
    return reduce(run_function, [[], ] + data_list)


def merge_nebula_value(data_list: list) -> dict:
    nodes = []
    relationships = []

    for data in data_list:
        nodes.extend(list(data.values())[0]["nodes"])
        relationships.extend(list(data.values())[0]["relationships"])
    result_dict = {"nodes": list_dict_duplicate_removal(nodes),
                   "relationships": list_dict_duplicate_removal(relationships)}
    return result_dict


def customized_cast_with_dict(val: ValueWrapper):
    _type = val._value.getType()
    method = cast_as.get(_type)
    if method is not None:
        value = getattr(val, method, lambda *args, **kwargs: None)()
        if isinstance(value, dict):
            for k, v in value.items():
                value[k] = customized_cast_with_dict(v)
        elif isinstance(value, list):
            for i, v in enumerate(value):
                value[i] = customized_cast_with_dict(v)
        elif isinstance(value, set):
            new_value = set()
            for v in value:
                new_value.add(customized_cast_with_dict(v))
            value = new_value
        elif isinstance(value, tuple):
            new_value = []
            for v in value:
                new_value.append(customized_cast_with_dict(v))
            value = tuple(new_value)
        elif isinstance(value, Relationship):
            value = {k: customized_cast_with_dict(v) for k, v in value.properties().items()}
        elif isinstance(value, PathWrapper):
            nodes = []
            relationships = []
            for node in value.nodes():
                vid = customized_cast_with_dict(node.get_id())
                for tag in node.tags():
                    point = {"_vid": vid, "_tag": tag}
                    point.update({k: customized_cast_with_dict(v) for k, v in node.properties(tag).items()})
                    nodes.append(point)
            for rel in value.relationships():
                relationship = {"_name": rel.edge_name(), "_start": customized_cast_with_dict(rel.start_vertex_id()),
                                "_end": customized_cast_with_dict(rel.end_vertex_id())}
                relationship.update({k: customized_cast_with_dict(v) for k, v in rel.properties().items()})
                relationships.append(relationship)
            value = {"nodes": nodes, "relationships": relationships}
        elif isinstance(value, Node):
            nodes = []
            for tag in value.tags():
                point = {"_vid": customized_cast_with_dict(value.get_id()), "_tag": tag}
                point.update({k: customized_cast_with_dict(v) for k, v in value.properties(tag).items()})
                nodes.append(point)
            value = {"nodes": nodes}
        elif isinstance(value, Null):
            value = None
        return value
    raise KeyError("No such key: {}".format(_type))


def convert(resp: ResultSet):
    assert resp.is_succeeded()
    value_list = []
    for recode in resp:
        record = recode
        if hasattr(recode, "keys"):
            record = {}
            for key in recode.keys():
                val = customized_cast_with_dict(recode.get_value_by_key(key))
                record[key] = val
        if record:
            value_list.append(record)
    return value_list
