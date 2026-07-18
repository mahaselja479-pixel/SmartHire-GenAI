from src.parsing.loader import extract_text_from_pdf
from src.parsing.resume_parser import parse_resume
from src.generate.interview_questions import generate_interview_questions

resume_path = "data/resumes/MAHA SELJA_VK_Resume.pdf"

text = extract_text_from_pdf(resume_path)

resume = parse_resume(text)

questions = generate_interview_questions(
    resume,
    "Python Full Stack Developer"
)

print(questions)