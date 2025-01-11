# Proyecto de API de Ingeniería de Datos

Este proyecto es una API de Ingeniería de Datos desarrollada con FastAPI, Docker y PostgreSQL. La API permite la gestión de empleados, departamentos y trabajos mediante diferentes endpoints, y admite la carga de datos a través de archivos CSV.

## Características

- Creación, lectura y gestión de empleados, departamentos y trabajos.
- Carga de datos mediante archivos CSV.
- Integración con una base de datos PostgreSQL.
- Uso de Docker para la contenedorización del proyecto.

## Requisitos previos

- Docker y Docker Compose instalados.
- Acceso a una terminal o línea de comandos.

## Estructura del Proyecto

```
API_Data_Engineer/
├── Dockerfile
├── docker-compose.yml
├── app.py
├── models.py
├── utils.py
├── database.py
├── files/               # Carpeta para almacenar los archivos CSV de prueba
├── tests/
│   └── test_app.py      # Pruebas unitarias
└── README.md            # Documentación del proyecto
```

## Instalación y Configuración

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/tu_usuario/API_Data_Engineer.git
cd API_Data_Engineer
```

### Paso 2: Configurar Docker Compose

Asegúrate de que el archivo `docker-compose.yml` esté configurado correctamente. Añade un volumen para la carpeta `files` que contiene los archivos CSV de prueba:

```yaml
volumes:
  - .:/app
  - "/c/Users/tu_usuario/OneDrive/Formatos propios/GitHub/API_Data_Engineer/file:/app/files"
```

### Paso 3: Construir y Ejecutar los Contenedores

Ejecuta los siguientes comandos para construir y levantar los contenedores:

```bash
docker-compose build
docker-compose up
```

### Paso 4: Acceder a la API

Una vez que los contenedores estén en ejecución, la API estará disponible en `http://localhost:8000`. Puedes acceder a la documentación interactiva en `http://localhost:8000/docs`.

## Uso de la API

### Endpoints Disponibles

- `GET /departments/`: Recupera todos los departamentos.
- `GET /jobs/`: Recupera todos los trabajos.
- `GET /employees/`: Recupera todos los empleados.
- `POST /employees/upload/`: Sube un archivo CSV con datos de empleados.
- `POST /departments/upload/`: Sube un archivo CSV con datos de departamentos.
- `POST /jobs/upload/`: Sube un archivo CSV con datos de trabajos.
- `GET /hires/quarterly/`: Obtiene contrataciones trimestrales.
- `GET /hires/above-average/`: Obtiene departamentos con contrataciones por encima del promedio.

### Cargar Datos desde Archivos CSV

Para cargar datos, envía un archivo CSV a los endpoints de carga usando herramientas como Postman o `curl`. Asegúrate de que los archivos CSV estén en la carpeta `files` y siguen el formato adecuado.

Ejemplo de carga usando `curl`:

```bash
curl -X POST "http://localhost:8000/employees/upload/" -F "file=@files/employees.csv"
```

## Pruebas

### Ejecución de Pruebas Unitarias

Las pruebas están en el archivo `tests/test_app.py`. Para ejecutar las pruebas, entra en la consola del contenedor `web` y ejecuta `pytest`:

```bash
docker exec -it app_container bash
pytest
```

## Solución de Problemas

- **Error de montaje de volúmen**: Verifica que la ruta en `docker-compose.yml` esté correctamente escrita y que Docker tenga acceso a la carpeta.
- **Problemas de conexión a la base de datos**: Asegúrate de que el contenedor `db` esté en ejecución y accesible desde el contenedor `web`.

## Contribuciones

Si deseas contribuir a este proyecto, por favor, crea un fork del repositorio, realiza tus cambios y envía un pull request.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Para más detalles, consulta el archivo `LICENSE`.

---

© 2025 Luis Carlos Sanchez Rubiano. Todos los derechos reservados.

