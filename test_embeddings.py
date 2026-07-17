from src.search.embedding import get_embedding

text = """
Python
React
Django
Machine Learning
"""

embedding = get_embedding(text)

print(type(embedding))
print("Vector Length:", len(embedding))
print("First 10 Values:")
print(embedding[:10])