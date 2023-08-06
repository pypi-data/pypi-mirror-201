import os
from playhouse.pool import PooledMySQLDatabase
from peewee import Model, CharField, IntegerField, MySQLDatabase


# 定义数据库连接池
def create_connection_pool(database, max_connections=8, stale_timeout=300, **kwargs):
    return PooledMySQLDatabase(database, max_connections=max_connections, stale_timeout=stale_timeout, **kwargs)


db = PooledMySQLDatabase(
    "mydatabase",
    max_connections=8,
    stale_timeout=300,
    user="myusername",
    password="mypassword",
    host="localhost",
    port=3306,
)


# 定义通用增删改查函数
def create_record(model_class, **kwargs):
    with db.atomic():
        record = model_class.create(**kwargs)
        return record.id


def update_record(model_class, record_id, **kwargs):
    with db.atomic():
        query = model_class.update(**kwargs).where(model_class.id == record_id)
        return query.execute()


def delete_record(model_class, record_id):
    with db.atomic():
        query = model_class.delete().where(model_class.id == record_id)
        return query.execute()


def get_records(model_class, *select_fields, **where):
    query = model_class.select(*select_fields)
    for key, value in where.items():
        query = query.where(getattr(model_class, key) == value)
    return query


# 使用通用函数操作 User 模型类
class User(Model):
    name = CharField()
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = db
        table_name = "users"


# 插入数据
user_id = create_record(User, name="Alice", email="alice@example.com", password="password")

# 查询数据
users = get_records(User, User.id, User.name, User.email, User.password, name="Alice")
for user in users:
    print(user.id, user.name, user.email, user.password)

# 更新数据
updated = update_record(User, user_id, name="Bob", password="new_password")
print(updated)

# 删除数据
deleted = delete_record(User, user_id)
print(deleted)
