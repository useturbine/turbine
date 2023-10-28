import random


def create_embedding():
    return [random.uniform(0, 1) for _ in range(1536)]


metadata = {
    "string": "value",
    "number": 123,
    "boolean": True,
    "list": ["a", "b", "c"],
}
