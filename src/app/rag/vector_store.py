import chromadb

# Connect to a Chroma database (in-memory)
db = chromadb.Client(Settings())

collection = db.get_or_create_collection("rubric")
