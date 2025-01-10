from sqlalchemy import text
from fastapi import Depends
from sqlalchemy.orm import Session
from .database import get_db

@app.get("/hires/quarterly/")
def get_quarterly_hires(db: Session = Depends(get_db)):
    query = text("""
        SELECT d.name AS department, j.name AS job,
               SUM(CASE WHEN EXTRACT(QUARTER FROM e.datetime) = 1 THEN 1 ELSE 0 END) AS Q1,
               SUM(CASE WHEN EXTRACT(QUARTER FROM e.datetime) = 2 THEN 1 ELSE 0 END) AS Q2,
               SUM(CASE WHEN EXTRACT(QUARTER FROM e.datetime) = 3 THEN 1 ELSE 0 END) AS Q3,
               SUM(CASE WHEN EXTRACT(QUARTER FROM e.datetime) = 4 THEN 1 ELSE 0 END) AS Q4
        FROM employees e
        JOIN departments d ON e.department_id = d.id
        JOIN jobs j ON e.job_id = j.id
        WHERE EXTRACT(YEAR FROM e.datetime) = 2021
        GROUP BY d.name, j.name
        ORDER BY d.name, j.name;
    """)
    result = db.execute(query)
    return result.fetchall()

@app.get("/hires/above-average/")
def get_above_average_hires(db: Session = Depends(get_db)):
    query = text("""
        WITH average_hires AS (
            SELECT AVG(hired_count) AS avg_hires
            FROM (
                SELECT d.id, COUNT(e.id) AS hired_count
                FROM employees e
                JOIN departments d ON e.department_id = d.id
                WHERE EXTRACT(YEAR FROM e.datetime) = 2021
                GROUP BY d.id
            ) hires
        )
        SELECT d.id, d.name AS department, COUNT(e.id) AS hired
        FROM employees e
        JOIN departments d ON e.department_id = d.id
        WHERE EXTRACT(YEAR FROM e.datetime) = 2021
        GROUP BY d.id, d.name
        HAVING COUNT(e.id) > (SELECT avg_hires FROM average_hires)
        ORDER BY hired DESC;
    """)
    result = db.execute(query)
    return result.fetchall()
