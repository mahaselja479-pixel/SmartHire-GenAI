import json
from sklearn.metrics.pairwise import cosine_similarity
from src.search.embedding import get_embedding


def recommend_jobs(resume_skills, job_file="data/jobs/jobs.json"):
    """
    Compare resume skills with job skills using embeddings
    and cosine similarity.
    """

    # Convert resume skills list to text
    resume_text = " ".join(resume_skills)

    # Resume embedding
    resume_embedding = get_embedding(resume_text).reshape(1, -1)

    # Load jobs
    with open(job_file, "r") as f:
        jobs = json.load(f)

    recommendations = []

    for job in jobs:

        job_skills = job["skills"]

        job_text = " ".join(job_skills)

        job_embedding = get_embedding(job_text).reshape(1, -1)

        score = cosine_similarity(
            resume_embedding,
            job_embedding
        )[0][0]
        score = max(0.0, score)

        missing_skills = list(
            set(job_skills) - set(resume_skills)
        )

        recommendations.append({
    "title": job["title"],
    "company": job["company"],
    "location": job.get("location", "N/A"),
    "skills": job["skills"],
   "match_score": round(score * 100, 2),
    "missing_skills": missing_skills
})

    recommendations.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return recommendations