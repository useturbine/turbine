# from vectordb.milvus.client import Client

# client = Client(host="localhost", port=19530, user="root", password="Milvus")
# client.drop_collection("test_collection")
# client.create_collection(name="test_collection", id_type="int", dimension=4)
# client.create_index(
#     collection_name="test_collection",
#     params={"index_type": "IVF_SQ8", "metric_type": "L2", "params": {"nlist": 2048}},
# )
# client.insert(
#     collection_name="test_collection",
#     data=[
#         [1, 2, 3, 4, 5, 6],
#         [
#             [0.1, 0.2, 0.3, 0.4],
#             [0.2, 0.3, 0.4, 0.5],
#             [0.3, 0.4, 0.5, 0.6],
#             [0.4, 0.5, 0.6, 0.7],
#             [0.5, 0.6, 0.7, 0.8],
#             [0.6, 0.7, 0.8, 0.9],
#         ],
#     ],
# )
# results = client.search(
#     collection_name="test_collection",
#     data=[[0.1, 0.2, 0.3, 0.4]],
#     limit=10,
#     params={"metric_type": "L2", "params": {"nprobe": 10}},
# )
# print(results)


# from datasource.postgres import PostgresDataSource

# pg_datasource = PostgresDataSource(
#     host="localhost",
#     database="postgres",
#     user="postgres",
#     password="example",
#     table="users",
#     port=5432,
#     pk_column="id",
#     updated_at_column="updated_at",
# )
# docs = pg_datasource.get_documents()
# print(list(docs))


from datasource.mongo import MongoDataSource

mongo_datasource = MongoDataSource(
    # uri="mongodb://user:pass@localhost:27017/",
    uri="mongodb+srv://sumitg:<pass>@cluster0.m1jbpl5.mongodb.net/",
    database="test",
    collection="users",
)
# docs = mongo_datasource.get_documents()
# print(list(docs))

changes = mongo_datasource.listen_for_updates()
for change in changes:
    print(change)