from sqlalchemy.orm import Session
from models import Department, Job

def create_department(db: Session, department_name: str):
    new_department = Department(name=department_name)
    db.add(new_department)
    db.commit()
    db.refresh(new_department)
    return new_department

def create_job(db: Session, job_name: str):
    new_job = Job(name=job_name)
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

def get_departments(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Department).offset(skip).limit(limit).all()

def get_jobs(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Job).offset(skip).limit(limit).all()
