# Employee Data API

This API allows uploading employee data via CSV files, inserts the data into a PostgreSQL database, and provides endpoints to retrieve specific metrics.

## Features

- Upload CSV files containing employee data.
- Insert up to 1000 rows in batch transactions.
- Retrieve quarterly hires and departments hiring above average.

## Setup

### Docker

Build and run the containers:

```bash
docker-compose up --build
