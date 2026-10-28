from datetime import date, datetime, timedelta
from . import db
from .models import User, Candidate, Company, Job, Application, Interview, Offer

def seed_demo():
    if User.query.first(): return
    u=User(name="Aarav Sharma",email="recruiter@demo.com",role="Recruiter"); u.set_password("Demo@123")
    db.session.add(u)
    companies=[]
    for i,(name,industry,city) in enumerate([("Infosys","IT Services","Pune"),("Tech Mahindra","Technology","Pune"),("Persistent Systems","Software","Pune"),("HCLTech","IT Services","Mumbai"),("TCS","Technology","Pune")],101):
        c=Company(code=f"COM{i}",name=name,industry=industry,location=city,hr_name="Anita Desai",hr_email=f"talent{i}@example.com"); db.session.add(c); companies.append(c)
    db.session.flush()
    candidates=[]
    sample=[("Rahul Patil","rahul@example.com","Java","Java, SQL, Git",68,0),("Priya Kulkarni","priya@example.com","Python","Python, SQL, Flask",78,0),("Amit Joshi","amit@example.com","Testing","Manual Testing, SQL",72,1),("Sneha Rao","sneha@example.com","Data Analytics","Python, Excel, SQL",81,0),("Vikram Shah","vikram@example.com","Java","Java, Spring, SQL",65,0),("Neha Singh","neha@example.com","Python","Python, Django, SQL",75,0),("Rohan Mehta","rohan@example.com","Testing","Selenium, Java, SQL",69,0),("Isha Nair","isha@example.com","Data Analytics","Python, Power BI, SQL",84,0)]
    for i,(name,email,tech,skills,score,backlogs) in enumerate(sample,1001):
        c=Candidate(code=f"CAN{i}",name=name,email=email,mobile=f"987654{i:04d}"[-10:],qualification="BE",college="Kiran Institute of Technology",passing_year=2025,percentage=score,backlogs=backlogs,technology=tech,skills=skills,location="Pune",status="ACTIVE"); db.session.add(c); candidates.append(c)
    db.session.flush()
    jobs=[]
    for i,(company,title,tech,skills,cutoff,pkg) in enumerate([(companies[0],"Associate Java Developer","Java","SQL, Git",60,4.5),(companies[1],"Python Developer","Python","SQL, Flask",65,5.0),(companies[2],"QA Engineer","Testing","SQL",60,4.0),(companies[3],"Data Analyst","Data Analytics","Python, SQL",70,5.5),(companies[4],"Graduate Engineer Trainee","Java","SQL",60,3.8),(companies[0],"Junior Backend Developer","Python","SQL",65,4.8)],1):
        j=Job(code=f"JOB-2026-{i:03d}",title=title,company=company,openings=10+i,location=company.location,min_package=pkg,max_package=pkg+1.5,qualification="BE,BTech,MCA",min_percentage=cutoff,min_passing_year=2024,max_passing_year=2026,max_backlogs=0,technology=tech,skills=skills,deadline=date.today()+timedelta(days=30),status="OPEN"); db.session.add(j); jobs.append(j)
    db.session.flush()
    for i,(c,j) in enumerate(zip(candidates,jobs),1001):
        ok=c.percentage>=j.min_percentage and c.backlogs<=j.max_backlogs
        a=Application(code=f"APP{i}",candidate=c,job=j,status="SHORTLISTED" if ok else "REJECTED"); db.session.add(a); db.session.flush()
        if i<1005:
            dt=datetime.now()+timedelta(days=i-1000,hours=2)
            db.session.add(Interview(code=f"INT{i}",application=a,round="Technical",scheduled_at=dt,mode="Online",interviewer="Hiring Team"))
    db.session.commit()
