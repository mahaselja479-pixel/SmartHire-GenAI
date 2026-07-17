import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Create Groq client
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def parse_resume(resume_text):

    prompt = f"""
You are an expert Resume Parser.

Extract the following information from the resume.

Return ONLY valid JSON.

{{
    "name": "",
    "email": "",
    "phone": "",
    "skills": [],
    "education": [],
    "experience": []
}}

Resume:
{resume_text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    print("========== LLM OUTPUT ==========")
    print(content)
    print("================================")

    # Remove markdown if present
    content = content.replace("```json", "").replace("```", "").strip()

    return json.loads(content)