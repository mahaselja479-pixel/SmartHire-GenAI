from src.parsing.loader import extract_text_from_pdf
from src.parsing.resume_parser import parse_resume

resume_path = "data/resumes/MAHA SELJA_VK_Resume.pdf"   # Change if your filename is different

text = extract_text_from_pdf(resume_path)

result = parse_resume(text)

print(result)