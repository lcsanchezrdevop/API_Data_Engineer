from datetime import datetime
import pandas as pd
from io import StringIO
from fastapi import HTTPException
from sqlalchemy.orm import Session
import models  # Asegúrate de importar tus modelos
import numpy as np

def validate_and_insert_data(file_contents: str, db: Session):
    # Leer el archivo CSV en un DataFrame
    df = pd.read_csv(StringIO(file_contents), header=None)
    df.columns = ['id', 'name', 'datetime', 'department_id', 'job_id']

    # Reemplazar NaN y valores infinitos por None
    df = df.applymap(lambda x: None if isinstance(x, float) and (pd.isna(x) or np.isinf(x)) else x)

    # Reemplazar "T" y "Z" en las fechas ISO
    df['datetime'] = df['datetime'].apply(
        lambda x: x.replace("T", " ").replace("Z", "") if isinstance(x, str) else x
    )

    # Dividir el DataFrame en lotes de hasta 1000 filas
    batch_size = 1000
    failed_batches = []  # Lista para registrar lotes con errores

    for start in range(0, len(df), batch_size):
        batch = df.iloc[start:start+batch_size]
        valid_rows = []
        
        for index, row in batch.iterrows():
            try:
                # Convertir la fecha en datetime
                date = datetime.fromisoformat(row['datetime']) if pd.notna(row['datetime']) else None
                
                # Manejar valores nulos de department_id y job_id
                department_id = int(row['department_id']) if pd.notna(row['department_id']) else None
                job_id = int(row['job_id']) if pd.notna(row['job_id']) else None

                # Validar la existencia de claves foráneas
                if department_id is not None:
                    department = db.query(models.Department).filter(models.Department.id == department_id).first()
                    if not department:
                        raise ValueError(f"Department with id {department_id} does not exist")
                
                if job_id is not None:
                    job = db.query(models.Job).filter(models.Job.id == job_id).first()
                    if not job:
                        raise ValueError(f"Job with id {job_id} does not exist")
                
                # Crear instancia del modelo Employee
                employee = models.Employee(
                    id=row['id'], 
                    name=row['name'], 
                    datetime=date, 
                    department_id=department_id, 
                    job_id=job_id
                )
                valid_rows.append(employee)
            
            except Exception as e:
                # Registrar el error y continuar con la siguiente fila
                failed_batches.append({'row_index': index, 'error': str(e)})

        # Insertar el lote de filas válidas en la base de datos
        if valid_rows:
            try:
                db.bulk_save_objects(valid_rows)  # Insertar en lote
                db.commit()
            except Exception as e:
                db.rollback()  # Rollback si ocurre un error
                failed_batches.append({'batch_start': start, 'error': str(e)})

    if failed_batches:
        return {"message": "Some batches failed to insert", "failed_batches": failed_batches}
    
    return {"message": "All batches inserted successfully"}
