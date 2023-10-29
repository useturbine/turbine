from pymilvus import DataType, FieldSchema, CollectionSchema, Collection, connections
from scripts.config import config


id_max_length = 128
dimension = 1536
name = "test_collection"
similarity_metric = "IP"


def main():
    connections.connect("default", uri=config.milvus_url, token=config.milvus_token)
    fields = [
        FieldSchema(
            name="id",
            dtype=DataType.VARCHAR,
            is_primary=True,
            auto_id=False,
            max_length=id_max_length,
        ),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dimension),
    ]
    schema = CollectionSchema(fields, enable_dynamic_field=True)
    collection = Collection(name, schema)
    collection.create_index(
        index_name="embedding_index",
        field_name="embedding",
        index_params={
            "index_type": "IVF_SQ8",
            "metric_type": similarity_metric,
            "params": {"nlist": 2048},
        },
    )


if __name__ == "__main__":
    main()
