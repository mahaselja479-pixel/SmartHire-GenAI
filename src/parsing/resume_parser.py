import json
import time
import streamlit as st
from openai import OpenAI, RateLimitError

# Create Groq client using Streamlit Secrets
client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)


def parse_resume(resume_text):

    # Limit resume text to avoid unnecessary token usage
    resume_text = resume_text[:12000]

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

    # Retry if Groq temporarily rate-limits the request
    for attempt in range(3):
        try:
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

            # Remove markdown if present
            content = (
                content
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

            return json.loads(content)

        except RateLimitError:
            if attempt < 2:
                time.sleep(5)
            else:
                return {
                    "error": "Groq API rate limit reached. Please wait a few minutes and try again."
                }

        except json.JSONDecodeError:
            return {
                "error": "The AI returned an invalid JSON response."
            }