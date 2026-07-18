from src.parsing.loader import extract_text_from_pdf
from src.parsing.resume_parser import parse_resume
from src.generate.cover_letter import generate_cover_letter

resume_path = "data/resumes/MAHA SELJA_VK_Resume.pdf"

text = extract_text_from_pdf(resume_path)

resume = parse_resume(text)

cover_letter = generate_cover_letter(
    resume,
    "Python Full Stack Developer",
    "Infosys"
)

print(cover_letter)