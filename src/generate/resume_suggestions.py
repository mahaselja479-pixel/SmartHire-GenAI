import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def improve_resume(resume_data):

    prompt = f"""
You are an expert Resume Reviewer.

Analyze the following resume.

Provide your response in the following format:

## Strengths
- ...

## Weaknesses
- ...

## Missing Skills
- ...

## Suggestions
- ...

## Overall Score
Score: X/10

Resume:
{resume_data}
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