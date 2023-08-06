import pymongo
from pymongo import database
from pymongo.results import InsertOneResult, InsertManyResult, UpdateResult, DeleteResult
from typing import List, Dict


def connect_mongodb_database(url: str, database_name: str) -> database.Database:
    """
    连接 MongoDB 数据库，并返回指定的数据库实例

    Args:
        url: 数据库地址
        database_name: 数据库名称

    Returns:
        返回 database.Database 对象，代表连接到的 MongoDB 数据库实例
    """
    if url is None:
        url = "mongodb://localhost:27017/"
        print("用户未提供地址，将使用默认地址: ", url)
    client = pymongo.MongoClient(url)
    return client[database_name]


def create_mongodb_collection(database: database.Database, collection_name: str) -> pymongo.collection.Collection:
    """
    在指定的 MongoDB 数据库中创建一个集合

    Args:
        database: database.Database 对象，代表要创建集合的数据库实例
        collection_name: 要创建的集合名称

    Returns:
        返回 pymongo.collection.Collection 对象，代表创建的 MongoDB 集合
    """
    return database[collection_name]


def insert_one(collection: pymongo.collection.Collection, doc: Dict) -> InsertOneResult:
    """
    向 MongoDB 集合中插入一条文档

    Args:
        collection: pymongo.collection.Collection 对象，代表要插入文档的 MongoDB 集合
        doc: 要插入的文档数据，一个 Python 字典对象

    Returns:
        返回 InsertOneResult 对象，代表插入操作的结果
    """
    return collection.insert_one(doc)


def insert_many(collection: pymongo.collection.Collection, docs: List[Dict]) -> InsertManyResult:
    """
    向 MongoDB 集合中插入多条文档

    Args:
        collection: pymongo.collection.Collection 对象，代表要插入文档的 MongoDB 集合
        docs: 要插入的多个文档数据，一个 Python 字典对象的列表

    Returns:
        返回 results.InsertManyResult 对象，代表插入操作的结果
    """
    return collection.insert_many(docs)


def find_one(collection: pymongo.collection.Collection) -> Dict:
    """
    查询 MongoDB 集合中的一条文档

    Args:
        collection: pymongo.collection.Collection 对象，代表要查询的 MongoDB 集合

    Returns:
        返回一个 Python 字典对象，代表查询到的 MongoDB 文档数据
    """
    return collection.find_one()


def find_all(collection: pymongo.collection.Collection) -> pymongo.cursor.Cursor:
    """
    查询 MongoDB 集合中的所有文档

    Args:
        collection: pymongo.collection.Collection 对象，代表要查询的 MongoDB 集合

    Returns:
        返回一个 pymongo.cursor.Cursor 对象，代表查询到的 MongoDB 文档的游标
    """
    return collection.find()


def find_by_query(collection: pymongo.collection.Collection, query: Dict) -> pymongo.cursor.Cursor:
    """
    根据查询条件查询 MongoDB 集合中的文档

    Args:
        collection: pymongo.collection.Collection 对象，代表要查询的 MongoDB 集合
        query: 查询条件，一个 Python 字典对象，例如 {"age": 30}

    Returns:
        返回一个 pymongo.cursor.Cursor 对象，代表
    """
    return collection.find(query)


def delete_one(collection: pymongo.collection.Collection, query: Dict) -> DeleteResult:
    """
    从 MongoDB 集合中删除一条文档

    Args:
        collection: pymongo.collection.Collection 对象，代表要删除文档的 MongoDB 集合
        query: 删除条件，一个 Python 字典对象，例如 {"name": "John"}

    Returns:
        返回 DeleteResult 对象，代表删除操作的结果
    """
    return collection.delete_one(query)


def delete_many(collection: pymongo.collection.Collection, query: Dict) -> DeleteResult:
    """
    从 MongoDB 集合中删除多条文档

    Args:
        collection: pymongo.collection.Collection 对象，代表要删除文档的 MongoDB 集合
        query: 删除条件，一个 Python 字典对象，例如 {"age": {"$gt": 25}}，若为{}，则删除所有文档

    Returns:
        返回 DeleteResult 对象，代表删除操作的结果
    """
    return collection.delete_many(query)


def update_one(collection: pymongo.collection.Collection, query: Dict, update: Dict) -> UpdateResult:
    """
    更新 MongoDB 集合中的一条文档

    Args:
        collection: pymongo.collection.Collection 对象，代表要更新文档的 MongoDB 集合
        query: 更新条件，一个 Python 字典对象，例如 {"name": "John"}
        update: 要更新的文档数据，一个 Python 字典对象，例如 {"$set": {"age": 25}}

    Returns:
        返回 UpdateResult 对象，代表更新操作的结果
    """
    return collection.update_one(query, update)


def update_many(collection: pymongo.collection.Collection, query: Dict, update: Dict) -> UpdateResult:
    """
    更新 MongoDB 集合中的多条文档

    Args:
        collection: pymongo.collection.Collection 对象，代表要更新文档的 MongoDB 集合
        query: 更新条件，一个 Python 字典对象，例如 {"age": {"$lt": 30}}
        update: 要更新的文档数据，一个 Python 字典对象，例如 {"$set": {"age": 30}}

    Returns:
        返回 UpdateResult 对象，代表更新操作的结果
    """
    return collection.update_many(query, update)
