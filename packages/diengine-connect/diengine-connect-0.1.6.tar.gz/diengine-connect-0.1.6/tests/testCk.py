import diengine_connect

client = diengine_connect.get_client(host='192.168.110.12', port=18044)
var = client.database
# print(client.command('SELECT timezone()'))
print(client.command('show tables'))
#
# create_table = """CREATE TABLE default.test_part
# (
#     `PARTKEY` Int32,
#     `NAME` String,
#     `MFGR` String,
#     `CATEGORY` String,
#     `BRAND` String,
#     `COLOR` String,
#     `TYPE` String,
#     `SIZE` Int32,
#     `CONTAINER` String
# )
# ENGINE = MergeTree
# ORDER BY PARTKEY"""
#
# result = client.command(create_table)
# print(result)

select = "select * from __mc_user_info"
result = client.command(select)
print(result)
