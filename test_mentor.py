from src.mentor.career_mentor import (
    load_knowledge,
    chunk_text,
    create_chunk_embeddings,
    retrieve_context
)

knowledge = load_knowledge()

chunks = chunk_text(knowledge)

embeddings = create_chunk_embeddings(chunks)

question = "What skills should I learn for Python Full Stack Developer?"

context = retrieve_context(
    question,
    chunks,
    embeddings
)

print("Question:")
print(question)

print("\nRetrieved Context:\n")
print(context)