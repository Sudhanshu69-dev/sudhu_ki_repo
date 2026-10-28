from sqlalchemy import or_
from . import db
from .models import Candidate, Application, Job

def eligibility(candidate, job):
    reasons = []
    allowed = [x.strip().lower() for x in job.qualification.split(",")]
    if candidate.qualification.lower() not in allowed: reasons.append("qualification does not match")
    if candidate.percentage < job.min_percentage: reasons.append(f"score is below {job.min_percentage:g}%")
    if not job.min_passing_year <= candidate.passing_year <= job.max_passing_year: reasons.append("passing year is outside the allowed range")
    if candidate.backlogs > job.max_backlogs: reasons.append("backlog count exceeds the limit")
    candidate_skills = {s.strip().lower() for s in (candidate.skills + "," + candidate.technology).split(",") if s.strip()}
    required_skills = {s.strip().lower() for s in (job.skills + "," + job.technology).split(",") if s.strip()}
    missing = required_skills - candidate_skills
    if missing: reasons.append("missing skills: " + ", ".join(sorted(missing)))
    if job.status != "OPEN": reasons.append("job is not open")
    return not reasons, reasons

def create_application(candidate, job):
    existing = Application.query.filter_by(candidate_id=candidate.id, job_id=job.id).first()
    if existing: return None, "This candidate has already applied for this job."
    ok, reasons = eligibility(candidate, job)
    app = Application(code=f"APP{Application.query.count()+1001:04d}", candidate=candidate, job=job, status="ELIGIBLE" if ok else "REJECTED")
    db.session.add(app)
    return app, ("Eligible" if ok else "Not eligible: " + "; ".join(reasons))

def search_candidates(query="", technology="", status=""):
    q = Candidate.query
    if query: q = q.filter(or_(Candidate.name.ilike(f"%{query}%"), Candidate.email.ilike(f"%{query}%"), Candidate.code.ilike(f"%{query}%")))
    if technology: q = q.filter_by(technology=technology)
    if status: q = q.filter_by(status=status)
    return q.order_by(Candidate.name).all()
