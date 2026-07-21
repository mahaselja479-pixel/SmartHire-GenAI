from src.parsing.loader import extract_text_from_pdf
from src.parsing.resume_parser import parse_resume
from src.generate.cover_letter import generate_cover_letter

text = extract_text_from_pdf("data/resumes/MAHA SELJA_VK_Resume.pdf")

resume = parse_resume(text)

letter = generate_cover_letter(
    resume,
    "Python Full Stack Developer"
)

print(letter)