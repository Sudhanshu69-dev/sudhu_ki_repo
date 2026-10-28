from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(160), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(30), nullable=False, default="Recruiter")
    def set_password(self, password): self.password_hash = generate_password_hash(password)
    def check_password(self, password): return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id): return db.session.get(User, int(user_id))

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False, index=True)
    email = db.Column(db.String(160), unique=True, nullable=False, index=True)
    mobile = db.Column(db.String(10), nullable=False)
    qualification = db.Column(db.String(60), nullable=False)
    college = db.Column(db.String(140), nullable=False)
    passing_year = db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    backlogs = db.Column(db.Integer, nullable=False, default=0)
    technology = db.Column(db.String(60), nullable=False, index=True)
    skills = db.Column(db.String(255), default="")
    location = db.Column(db.String(100), default="")
    status = db.Column(db.String(24), nullable=False, default="ACTIVE", index=True)
    applications = db.relationship("Application", back_populates="candidate", cascade="all, delete-orphan")

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(140), nullable=False, unique=True, index=True)
    industry = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(200), default="")
    location = db.Column(db.String(100), nullable=False)
    hr_name = db.Column(db.String(100), nullable=False)
    hr_email = db.Column(db.String(160), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="ACTIVE")
    jobs = db.relationship("Job", back_populates="company")

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(30), unique=True, nullable=False, index=True)
    title = db.Column(db.String(140), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    openings = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    min_package = db.Column(db.Float, default=0)
    max_package = db.Column(db.Float, default=0)
    qualification = db.Column(db.String(100), nullable=False)
    min_percentage = db.Column(db.Float, nullable=False, default=0)
    min_passing_year = db.Column(db.Integer, default=0)
    max_passing_year = db.Column(db.Integer, default=9999)
    max_backlogs = db.Column(db.Integer, nullable=False, default=0)
    technology = db.Column(db.String(60), nullable=False)
    skills = db.Column(db.String(255), default="")
    deadline = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), nullable=False, default="OPEN", index=True)
    company = db.relationship("Company", back_populates="jobs")
    applications = db.relationship("Application", back_populates="job", cascade="all, delete-orphan")

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey("candidate.id"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("job.id"), nullable=False)
    status = db.Column(db.String(30), nullable=False, default="APPLIED", index=True)
    applied_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    candidate = db.relationship("Candidate", back_populates="applications")
    job = db.relationship("Job", back_populates="applications")
    interview = db.relationship("Interview", back_populates="application", uselist=False, cascade="all, delete-orphan")
    __table_args__ = (db.UniqueConstraint("candidate_id", "job_id", name="unique_candidate_job_application"),)

class Interview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    application_id = db.Column(db.Integer, db.ForeignKey("application.id"), nullable=False, unique=True)
    round = db.Column(db.String(30), nullable=False, default="Technical")
    scheduled_at = db.Column(db.DateTime, nullable=False)
    mode = db.Column(db.String(20), nullable=False, default="Online")
    interviewer = db.Column(db.String(100), default="")
    status = db.Column(db.String(24), nullable=False, default="SCHEDULED")
    feedback = db.Column(db.String(500), default="")
    rating = db.Column(db.Integer, nullable=True)
    application = db.relationship("Application", back_populates="interview")

class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey("application.id"), nullable=False, unique=True)
    designation = db.Column(db.String(120), nullable=False)
    package = db.Column(db.Float, nullable=False)
    joining_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(24), nullable=False, default="OFFERED")
    application = db.relationship("Application")
