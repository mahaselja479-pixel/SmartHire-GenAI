from src.parsing.loader import extract_text_from_pdf
from src.parsing.resume_parser import parse_resume
from src.search.job_matcher import recommend_jobs

resume_path = "data/resumes/MAHA SELJA_VK_Resume.pdf"

text = extract_text_from_pdf(resume_path)

resume = parse_resume(text)

jobs = recommend_jobs(resume["skills"])

print("\nRecommended Jobs\n")

for job in jobs:
    print(job)