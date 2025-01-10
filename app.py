from fastapi import FastAPI, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
import pandas as pd
from datetime import datetime
import boto3
from database import SessionLocal, engine
import models
from io import StringIO

app = FastAPI()

# Crea las tablas en la base de datos si no existen
models.Base.metadata.create_all(bind=engine)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

@app.get("/departments/")
def read_departments(db: Session = Depends(get_db)):
    return db.query(models.Department).all()

@app.get("/jobs/")
def read_jobs(db: Session = Depends(get_db)):
    return db.query(models.Job).all()

@app.get("/employees/")
def read_employees(db: Session = Depends(get_db)):
    employees = db.query(models.Employee).all()  # Consulta a la tabla Employee
    return employees  # Devuelve los resultados

# Endpoint para cargar empleados desde un archivo CSV
@app.post("/upload/")
async def upload_file(file: UploadFile, db: Session = Depends(get_db)):
    try:
        contents = await file.read()
        
        # Process and save file to S3 (AWS configuration required)
        # s3 = boto3.client('s3', aws_access_key_id='your_key', aws_secret_access_key='your_secret')
        # s3.put_object(Bucket='your_bucket', Key=file.filename, Body=contents)
        
        # Carga el archivo CSV sin encabezado (header=None)
        file_str = contents.decode('utf-8')
        df = pd.read_csv(StringIO(file_str), header=None)

        # Asignar nombres de columnas manualmente
        df.columns = ['id', 'name', 'datetime', 'department_id', 'job_id']

        # Asegurarse de que la columna datetime sea tipo string antes de procesar
        df['datetime'] = df['datetime'].astype(str)

        # Reemplazar el "Z" al final de las fechas ISO si existe
        df['datetime'] = df['datetime'].apply(lambda x: x.replace("Z", "") if isinstance(x, str) else x)
        
        # Verificación antes de la conversión de las fechas
        print("Valores antes de la conversión:")
        print(df['datetime'])

        # Convertir valores válidos en datetime y los valores NaT se dejan como None
        df['datetime'] = df['datetime'].apply(
            lambda x: datetime.fromisoformat(x) if x.lower() != 'nan' and x != '' and x != 'NaT' else None
        )

        # Verificación después de la conversión
        print("Valores después de la conversión:")
        print(df['datetime'])

        # Inserta los datos en la base de datos
        for index, row in df.iterrows():
            employee = models.Employee(
                id=row['id'], 
                name=row['name'], 
                datetime=row['datetime'] if row['datetime'] is not None else None,  # Se inserta NULL si la fecha es None 
                department_id=row['department_id'], 
                job_id=row['job_id']
            )
            db.add(employee)
        db.commit()
        
        return {"message": "File uploaded and data inserted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para cargar departamentos desde un archivo CSV
@app.post("/departments/upload/")
async def upload_departments(file: UploadFile, db: Session = Depends(get_db)):
    try:
        # Leer el archivo CSV
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode('utf-8')), header=None)

        # Asignar nombres de columnas manualmente
        df.columns = ['id', 'name']
        
        # Insertar datos de departamentos
        for _, row in df.iterrows():
            db_department = models.Department(name=row['name'])
            db.add(db_department)
        
        db.commit()
        return {"message": "Departments uploaded successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para cargar trabajos desde un archivo CSV
@app.post("/jobs/upload/")
async def upload_jobs(file: UploadFile, db: Session = Depends(get_db)):
    try:
        # Leer el archivo CSV
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode('utf-8')), header=None)

        # Asignar nombres de columnas manualmente
        df.columns = ['id', 'title']
        
        # Insertar datos de trabajos
        for _, row in df.iterrows():
            db_job = models.Job(title=row['title'])
            db.add(db_job)
        
        db.commit()
        return {"message": "Jobs uploaded successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))