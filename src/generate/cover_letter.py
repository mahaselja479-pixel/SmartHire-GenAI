import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def generate_cover_letter(resume_data, job_title, company):

    prompt = f"""
You are a professional HR expert.

Generate a professional cover letter.

Candidate Resume:
{resume_data}

Job Title:
{job_title}

Company:
{company}

Instructions:
- Professional tone
- Around 250 words
- Mention candidate skills
- Explain why the candidate fits the role
- End politely
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.5
    )

    return response.choices[0].message.content