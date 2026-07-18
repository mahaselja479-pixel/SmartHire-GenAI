from src.mentor.career_mentor import load_knowledge
from src.mentor.career_mentor import chunk_text

knowledge = load_knowledge()

chunks = chunk_text(knowledge)

print("Number of Chunks:", len(chunks))

print("\nFirst Chunk:\n")
print(chunks[0])