# RecruitFlow — Recruitment & Placement Management System

A full-stack student project built with Python, Flask, SQLAlchemy, HTML, and CSS. It follows the supplied UI prototype specification while connecting the screens to a working backend.

## Features

- Responsive 12-screen workflow: login, dashboard, candidates, candidate form and profile, companies, jobs and job form, applications, interviews, placement process, and reports.
- Role-aware demo sign-in, password hashing, protected pages, and clean logout.
- Candidate directory search, profile management, and server-side field validation.
- Job criteria and automatic eligibility checks for qualification, percentage, passing year, backlogs, technology, and skills.
- Duplicate application prevention, application status changes, interview scheduling, interview feedback, offers, joining status, and summary reports.
- SQLite by default for quick local startup; MySQL works by setting `DATABASE_URL`.
- No external frontend framework or build step required.

## Run locally

Requires Python 3.10 or later.

```powershell
cd recruitment-placement
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python run.py
```

Open <http://127.0.0.1:5000>.

Demo login: `recruiter@demo.com` / `Demo@123`.

The first run creates the database and sample records. SQLite is stored in Flask's local `instance/` directory. Seed records are added only when no user exists.

## MySQL setup

Create an empty database, then update `.env`:

```dotenv
SECRET_KEY=replace-with-a-long-random-secret
DATABASE_URL=mysql+pymysql://username:password@localhost/recruitment_db?charset=utf8mb4
```

Install requirements and start with `python run.py`. For deployment, set `SECRET_KEY` to a unique random value, set `FLASK_DEBUG=0`, run behind a production WSGI server, and apply schema changes through migrations rather than relying on `create_all`.

## Project structure

```text
recruitment-placement/
├── app/
│   ├── models.py        # SQLAlchemy data models
│   ├── routes.py        # Page routes and workflow actions
│   ├── services.py      # Eligibility and search logic
│   ├── seed.py          # Demo content
│   ├── templates/       # Jinja HTML pages
│   └── static/css/      # Shared responsive styling
├── .env.example
├── requirements.txt
└── run.py
```

## Notes

- Demo credentials are for local evaluation. Change the demo password and secret before exposing the app to a network.
- Employment type is currently a presentation-only field; core hiring, eligibility, interview, offer, and joining workflows are stored in the database.
- The project uses a simple schema bootstrap to make first startup easy. Use Flask-Migrate/Alembic before evolving a populated deployment database.
