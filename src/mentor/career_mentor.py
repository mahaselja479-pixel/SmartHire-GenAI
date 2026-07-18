from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load embedding model only once
model = SentenceTransformer("all-MiniLM-L6-v2")


def load_knowledge(file_path="data/knowledge/career_guide.txt"):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def chunk_text(text, chunk_size=200):
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    return chunks


def create_chunk_embeddings(chunks):
    embeddings = model.encode(chunks)

    return embeddings
def retrieve_context(question, chunks, embeddings):
    
    # Convert question into embedding
    question_embedding = model.encode([question])

    # Compare with all chunk embeddings
    scores = cosine_similarity(
        question_embedding,
        embeddings
    )[0]

    # Best matching chunk
    best_index = scores.argmax()

    return chunks[best_index]