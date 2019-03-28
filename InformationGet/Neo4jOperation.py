# -*- coding: utf-8 -*-
"""
@File  : Neo4jOperation.py
@Author: SangYu
@Date  : 2018/12/28 13:29
@Desc  : Neo4j数据库操作
"""
if __name__ == "__main__":
    from py2neo import Graph, Node, Relationship

    graph = Graph("http://127.0.0.1:7474", username="neo4j", password="123456")
    graph.delete_all()
    a = Node('Person', name='Alice')
    b = Node('Person', name='Bob')
    r = Relationship(a, 'KNOWS', b)
    a['age'] = 20
    b['age'] = 21
    r['time'] = '2017/08/31'
    a.setdefault('location', '北京')
    s = a | b | r
    graph.create(s)
    print(a, b, r)
