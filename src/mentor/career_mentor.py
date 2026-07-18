from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

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

def ask_career_mentor(question, chunks, embeddings):
    
    context = retrieve_context(
        question,
        chunks,
        embeddings
    )

    prompt = f"""
You are an AI Career Mentor.

Answer the user's question using ONLY the provided context.

If the answer is not available in the context, say:
"I don't have enough information in my knowledge base."

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content