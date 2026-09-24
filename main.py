from sentence_transformers import SentenceTransformer
import chromadb


# STEP 1 — LOAD DOCUMENT


with open("sample.txt", "r", encoding="utf-8") as file:
    text = file.read()

print("Document loaded successfully!")
print(text)



# STEP 2 — TEXT CHUNKING


chunk_size = 100
overlap = 20

chunks = []

start = 0

while start < len(text):
    end = start + chunk_size

    chunk = text[start:end]

    chunks.append(chunk)

    start += chunk_size - overlap


print("\nChunks:")
for i, chunk in enumerate(chunks):
    print(f"\nChunk {i}:")
    print(chunk)



# STEP 3 — CREATE EMBEDDINGS


model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(chunks)

print("\nEmbedding created!")

print("Number of chunks:", len(chunks))
print("Embedding size:", len(embeddings[0]))



# STEP 4 — VECTOR DATABASE


client = chromadb.Client()

collection = client.get_or_create_collection(
    name="crypto_knowledge"
)


# Store chunks + embeddings

collection.add(
    ids=[f"chunk_{i}" for i in range(len(chunks))],
    documents=chunks,
    embeddings=embeddings.tolist()
)

print("\nData stored in Chroma!")



# STEP 5 — RETRIEVAL


query = "How does liquidity affect Bitcoin?"

query_embedding = model.encode([query])


results = collection.query(
    query_embeddings=query_embedding.tolist(),
    n_results=3
)


print("\nUser Question:")
print(query)


print("\nRetrieved Chunks:")

for i, document in enumerate(results["documents"][0]):
    print(f"\nResult {i + 1}:")
    print(document)