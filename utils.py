from datetime import datetime
import pandas as pd
from io import StringIO
from fastapi import HTTPException
from sqlalchemy.orm import Session
import models  # Asegúrate de importar tus modelos
import numpy as np

def validate_and_insert_data(file_contents: str, db: Session):
    # Leer el archivo CSV
    df = pd.read_csv(StringIO(file_contents), header=None)

    if isinstance(df, pd.DataFrame):
        # Reemplazar NaN y valores infinitos por None
        df = df.applymap(lambda x: None if isinstance(x, float) and (pd.isna(x) or np.isinf(x)) else x)

    # Asignar nombres de columnas manualmente
    df.columns = ['id', 'name', 'datetime', 'department_id', 'job_id']

    # Reemplazar "T" y "Z" en las fechas ISO
    df['datetime'] = df['datetime'].apply(
        lambda x: x.replace("T", " ").replace("Z", "") if isinstance(x, str) else x
    )

    # Validar cada fila y agregarla a la base de datos si es válida
    failed_rows = []  # Lista para guardar registros que no se pudieron insertar

    for index, row in df.iterrows():
        try:
            # Convertir la fecha en datetime
            if row['datetime']:
                try:
                    date = datetime.fromisoformat(row['datetime']) if row['datetime'] != 'NaT' else None
                except ValueError as e:
                    date = None
            else:
                date = None

            # Manejar valores nulos de department_id y job_id
            department_id = int(row['department_id']) if pd.notna(row['department_id']) else None
            job_id = int(row['job_id']) if pd.notna(row['job_id']) else None

            # Verificar si department_id y job_id existen en las tablas correspondientes
            if department_id is not None:
                department = db.query(models.Department).filter(models.Department.id == department_id).first()
                if not department:
                    raise ValueError(f"Department with id {department_id} does not exist")

            if job_id is not None:
                job = db.query(models.Job).filter(models.Job.id == job_id).first()
                if not job:
                    raise ValueError(f"Job with id {job_id} does not exist")

            # Insertar el registro en la base de datos
            employee = models.Employee(
                id=row['id'], 
                name=row['name'], 
                datetime=date, 
                department_id=department_id,  # Puede ser None si es nulo
                job_id=job_id  # Puede ser None si es nulo
            )

            db.add(employee)
            db.flush()  # Asegúrate de que el registro se haya insertado correctamente
        except Exception as e:
            failed_rows.append({'row': row, 'error': str(e)})  # Si falla, agregar a los fallos

    # Intentar hacer commit de todos los registros válidos
    try:
        db.commit()
    except Exception as e:
        db.rollback()  # Rollback si ocurre un error en el commit

    if failed_rows:
        return {"message": "Some rows failed to insert", "failed_rows": failed_rows}
    
    return {"message": "File uploaded and data inserted successfully"}
