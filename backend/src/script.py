from src.datasource.postgres import Postgres
from src.vectordb.milvus.client import Client
from pymilvus import DataType

# get data from your chosen integration
data = Postgres.read_table(
    host="localhost",
    database="postgres",
    user="postgres",
    password="example",
    table="test",
)

# create a client for milvus as vector db
client = Client(uri="tcp://localhost:19530", user="root", password="example")

# create a collection
dimension = 128
client.create_collection(
    "collection1",
    params={
        "fields": [
            {
                "name": "vector",
                "type": DataType.FLOAT_VECTOR,
                "params": {"dim": 128},
                "indexes": [{"metric_type": "L2"}],
            }
        ],
        "segment_row_count": 4096,
        "auto_id": True,
    },
)

# insert data into collection
client.insert(
    collection="collection1",
    params={
        "fields": [{"name": "vector", "type": DataType.FLOAT_VECTOR, "values": data}]
    },
)

# create index for collection
# https://milvus.io/docs/v2.0.x/build_index.md
client.create_index(
    collection="collection1",
    field="vector",
    params={"index_type": "IVF_SQ8", "metric_type": "L2", "params": {"nlist": 2048}},
    index_name="index1",
)


# search on top of index
query_embedding = []  # query here
top_k = 10
results = client.search(
    collection="collection1",
    field="vector",
    data=query_embedding,
    top_k=top_k,
    params={"metric_type": "L2", "params": {"nprobe": 10}},
)

# print results
