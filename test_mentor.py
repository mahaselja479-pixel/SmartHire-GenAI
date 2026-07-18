from src.mentor.career_mentor import (
    load_knowledge,
    chunk_text,
    create_chunk_embeddings,
    ask_career_mentor
)

knowledge = load_knowledge()

chunks = chunk_text(knowledge)

embeddings = create_chunk_embeddings(chunks)

question = input("Ask Career Mentor: ")

answer = ask_career_mentor(
    question,
    chunks,
    embeddings
)

print("\n========== AI Career Mentor ==========\n")
print(answer)