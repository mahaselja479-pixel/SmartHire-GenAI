from src.parsing.loader import extract_text_from_pdf

resume_path = "data/resumes/MAHA SELJA_VK_Resume.pdf"

text = extract_text_from_pdf(resume_path)

print(text)