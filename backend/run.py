from turbine.embedding_model import get_embedding_model

model = get_embedding_model("all-MiniLM-L6-v2")
embedding = model.model.get_embedding("Hello world!")
print(embedding)
