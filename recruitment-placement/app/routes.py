from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import func
from . import db
from .models import User, Candidate, Company, Job, Application, Interview, Offer
from .services import search_candidates, create_application

auth = Blueprint("auth", __name__)
main = Blueprint("main", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated: return redirect(url_for("main.dashboard"))
    if request.method == "POST":
        user = User.query.filter_by(email=request.form.get("email", "").strip().lower()).first()
        if user and user.check_password(request.form.get("password", "")):
            login_user(user); return redirect(url_for("main.dashboard"))
        flash("Email or password is incorrect.", "error")
    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user(); return redirect(url_for("auth.login"))

@main.route("/")
def home(): return redirect(url_for("main.dashboard")) if current_user.is_authenticated else redirect(url_for("auth.login"))

@main.route("/dashboard")
@login_required
def dashboard():
    counts = {"candidates": Candidate.query.count(), "active": Candidate.query.filter_by(status="ACTIVE").count(), "companies": Company.query.filter_by(status="ACTIVE").count(), "jobs": Job.query.filter_by(status="OPEN").count(), "applications": Application.query.count(), "interviews": Interview.query.filter_by(status="SCHEDULED").count(), "selected": Application.query.filter_by(status="SELECTED").count(), "placed": Offer.query.filter_by(status="JOINED").count()}
    return render_template("dashboard.html", counts=counts, interviews=Interview.query.order_by(Interview.scheduled_at).limit(5).all(), jobs=Job.query.filter_by(status="OPEN").order_by(Job.id.desc()).limit(5).all())

@main.route("/candidates")
@login_required
def candidates():
    rows = search_candidates(request.args.get("q", "").strip(), request.args.get("technology", ""), request.args.get("status", ""))
    return render_template("candidates.html", candidates=rows, q=request.args.get("q", ""), technology=request.args.get("technology", ""), status=request.args.get("status", ""))

@main.route("/candidates/new", methods=["GET", "POST"])
@main.route("/candidates/<int:candidate_id>/edit", methods=["GET", "POST"])
@login_required
def candidate_form(candidate_id=None):
    item = db.session.get(Candidate, candidate_id) if candidate_id else Candidate()
    if candidate_id and not item: flash("Candidate not found.", "error"); return redirect(url_for("main.candidates"))
    if request.method == "POST":
        f = request.form
        try:
            item.name=f["name"].strip(); item.email=f["email"].strip().lower(); item.mobile=f["mobile"].strip()
            item.qualification=f["qualification"]; item.college=f["college"].strip(); item.passing_year=int(f["passing_year"])
            item.percentage=float(f["percentage"]); item.backlogs=int(f["backlogs"]); item.technology=f["technology"]
            item.skills=f.get("skills", "").strip(); item.location=f.get("location", "").strip(); item.status=f["status"]
            if len(item.mobile) != 10 or not item.mobile.isdigit(): raise ValueError("Mobile number must contain 10 digits.")
            if not 0 <= item.percentage <= 100: raise ValueError("Percentage must be between 0 and 100.")
            if item.passing_year < 1990 or item.passing_year > date.today().year + 8: raise ValueError("Enter a valid passing year.")
            duplicate = Candidate.query.filter(func.lower(Candidate.email)==item.email, Candidate.id != (item.id or 0)).first()
            if duplicate: raise ValueError("A candidate with this email already exists.")
            if not item.id: item.code=f"CAN{Candidate.query.count()+1001:04d}"; db.session.add(item)
            db.session.commit(); flash("Candidate saved successfully.", "success"); return redirect(url_for("main.candidates"))
        except (ValueError, KeyError) as e: db.session.rollback(); flash(str(e) or "Please check the form fields.", "error")
    return render_template("candidate_form.html", candidate=item)

@main.route("/candidates/<int:candidate_id>")
@login_required
def candidate_details(candidate_id):
    item=db.session.get(Candidate,candidate_id)
    if not item: flash("Candidate not found.", "error"); return redirect(url_for("main.candidates"))
    return render_template("candidate_details.html", candidate=item)

@main.route("/companies", methods=["GET", "POST"])
@login_required
def companies():
    if request.method == "POST":
        f=request.form
        try:
            c=Company(code=f"COM{Company.query.count()+101:03d}", name=f["name"].strip(), industry=f["industry"].strip(), website=f.get("website", "").strip(), location=f["location"].strip(), hr_name=f["hr_name"].strip(), hr_email=f["hr_email"].strip().lower(), status="ACTIVE")
            db.session.add(c); db.session.commit(); flash("Company added.", "success")
        except Exception: db.session.rollback(); flash("Could not add company. Check that its name is unique and all required fields are valid.", "error")
        return redirect(url_for("main.companies"))
    return render_template("companies.html", companies=Company.query.order_by(Company.name).all())

@main.route("/jobs")
@login_required
def jobs(): return render_template("jobs.html", jobs=Job.query.order_by(Job.id.desc()).all())

@main.route("/jobs/new", methods=["GET", "POST"])
@main.route("/jobs/<int:job_id>/edit", methods=["GET", "POST"])
@login_required
def job_form(job_id=None):
    item=db.session.get(Job, job_id) if job_id else Job()
    if job_id and not item: flash("Job not found.", "error"); return redirect(url_for("main.jobs"))
    companies=Company.query.filter_by(status="ACTIVE").order_by(Company.name).all()
    if request.method == "POST":
        f=request.form
        try:
            item.company_id=int(f["company_id"]); item.code=f["code"].strip().upper(); item.title=f["title"].strip(); item.openings=int(f["openings"]); item.location=f["location"].strip()
            item.min_package=float(f.get("min_package") or 0); item.max_package=float(f.get("max_package") or 0); item.qualification=f["qualification"]; item.min_percentage=float(f["min_percentage"])
            item.min_passing_year=int(f.get("min_passing_year") or 0); item.max_passing_year=int(f.get("max_passing_year") or 9999); item.max_backlogs=int(f["max_backlogs"]); item.technology=f["technology"]; item.skills=f.get("skills", "").strip()
            item.deadline=datetime.strptime(f["deadline"], "%Y-%m-%d").date() if f.get("deadline") else None; item.status=f["status"]
            if item.openings < 1: raise ValueError("Number of openings must be greater than zero.")
            if item.min_package > item.max_package and item.max_package: raise ValueError("Minimum package cannot exceed maximum package.")
            if item.max_passing_year < item.min_passing_year: raise ValueError("Maximum passing year must be after minimum year.")
            if not item.id: db.session.add(item)
            db.session.commit(); flash("Job saved successfully.", "success"); return redirect(url_for("main.jobs"))
        except (ValueError, KeyError) as e: db.session.rollback(); flash(str(e) or "Please check the job details.", "error")
    return render_template("job_form.html", job=item, companies=companies)

@main.route("/applications", methods=["GET", "POST"])
@login_required
def applications():
    if request.method == "POST":
        candidate=db.session.get(Candidate, int(request.form.get("candidate_id", 0))); job=db.session.get(Job, int(request.form.get("job_id", 0)))
        if not candidate or not job: flash("Select a valid candidate and job.", "error")
        else:
            app, message=create_application(candidate,job)
            if app: db.session.add(app); db.session.commit(); flash(message, "success" if app.status=="ELIGIBLE" else "info")
            else: flash(message,"error")
        return redirect(url_for("main.applications"))
    rows=Application.query.order_by(Application.applied_at.desc()).all()
    return render_template("applications.html", applications=rows, candidates=Candidate.query.filter_by(status="ACTIVE").all(), jobs=Job.query.filter_by(status="OPEN").all())

@main.route("/applications/<int:application_id>/status/<status>", methods=["POST"])
@login_required
def application_status(application_id,status):
    app=db.session.get(Application,application_id)
    allowed={"SHORTLISTED","REJECTED","SELECTED"}
    if not app or status not in allowed: flash("That application action is not valid.","error")
    else: app.status=status; db.session.commit(); flash(f"Application marked {status.lower()}.","success")
    return redirect(url_for("main.applications"))

@main.route("/interviews", methods=["GET", "POST"])
@login_required
def interviews():
    if request.method == "POST":
        try:
            app=db.session.get(Application,int(request.form["application_id"]))
            scheduled=datetime.strptime(request.form["scheduled_at"],"%Y-%m-%dT%H:%M")
            if scheduled < datetime.now(): raise ValueError("Interview date cannot be in the past.")
            if not app: raise ValueError("Select an application.")
            i=Interview(code=f"INT{Interview.query.count()+1001:04d}",application=app,round=request.form["round"],scheduled_at=scheduled,mode=request.form["mode"],interviewer=request.form.get("interviewer", ""))
            app.status="INTERVIEW_SCHEDULED"; db.session.add(i); db.session.commit(); flash("Interview scheduled.","success")
        except (ValueError,KeyError) as e: db.session.rollback(); flash(str(e),"error")
        return redirect(url_for("main.interviews"))
    return render_template("interviews.html", interviews=Interview.query.order_by(Interview.scheduled_at).all(), applications=Application.query.filter(Application.status.in_(["ELIGIBLE","SHORTLISTED"])).all())

@main.route("/interviews/<int:interview_id>/feedback", methods=["POST"])
@login_required
def interview_feedback(interview_id):
    item=db.session.get(Interview,interview_id)
    if item:
        try:
            item.feedback=request.form.get("feedback", "").strip(); item.rating=int(request.form["rating"]); result=request.form["result"]
            if item.rating not in range(1,6): raise ValueError()
            item.status="COMPLETED"; item.application.status=result
            if result=="SELECTED" and not Offer.query.filter_by(application_id=item.application_id).first():
                db.session.add(Offer(application_id=item.application_id,designation=item.application.job.title,package=item.application.job.min_package or item.application.job.max_package or 0,status="OFFERED"))
            db.session.commit(); flash("Interview feedback saved.","success")
        except (ValueError,KeyError): db.session.rollback(); flash("Choose a rating from 1 to 5 and a result.","error")
    return redirect(url_for("main.interviews"))

@main.route("/placements", methods=["GET", "POST"])
@login_required
def placements():
    if request.method=="POST":
        offer=db.session.get(Offer,int(request.form.get("offer_id",0)))
        status=request.form.get("status")
        if offer and status in {"ACCEPTED","REJECTED","JOINED","NOT_JOINED"}:
            offer.status=status
            if status in {"JOINED","NOT_JOINED"}: offer.application.status=status
            db.session.commit(); flash("Offer status updated.","success")
        else: flash("Choose a valid offer and status.","error")
        return redirect(url_for("main.placements"))
    return render_template("placements.html",offers=Offer.query.order_by(Offer.id.desc()).all())

@main.route("/reports")
@login_required
def reports():
    selected=Application.query.filter_by(status="SELECTED").count(); joined=Offer.query.filter_by(status="JOINED").count(); total=Application.query.count()
    company_rows=db.session.query(Company.name,func.count(Offer.id)).join(Job,Job.company_id==Company.id).join(Application,Application.job_id==Job.id).join(Offer,Offer.application_id==Application.id).filter(Offer.status=="JOINED").group_by(Company.name).all()
    return render_template("reports.html", total=total, interviews=Interview.query.count(), selected=selected, joined=joined, rate=round(joined/max(selected,1)*100,1), company_rows=company_rows)
