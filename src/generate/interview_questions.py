import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def generate_interview_questions(resume_data, job_title):

    prompt = f"""
You are an experienced Technical Interviewer.

Candidate Resume:
{resume_data}

Target Job:
{job_title}

Generate interview questions in this format:

# Technical Questions
1.
2.
3.
4.
5.

# HR Questions
1.
2.
3.

# Coding Questions
1.
2.
3.

# Project-Based Questions
1.
2.
3.

Keep the questions specific to the candidate's resume and the target job.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4
    )

    return response.choices[0].message.content