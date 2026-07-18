from src.parsing.loader import extract_text_from_pdf
from src.parsing.resume_parser import parse_resume
from src.generate.resume_suggestions import improve_resume

resume_path = "data/resumes/MAHA SELJA_VK_Resume.pdf"

text = extract_text_from_pdf(resume_path)

resume = parse_resume(text)

result = improve_resume(resume)

print(result)