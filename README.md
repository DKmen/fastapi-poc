# FastAPI POC Project

This is a proof of concept project built with FastAPI demonstrating best practices for building scalable APIs.


## Demo Video

[View Demo Video](/demo.mp4)

## Project Description

This project implements:
- RESTful API endpoints using FastAPI
- PostgreSQL database integration
- SQLAlchemy ORM for database operations
- Alembic for database migrations
- JWT authentication
- Docker containerization
- API documentation with Swagger UI
- Unit tests with pytest

## Folder Structure

```
├── app
│   ├── __init__.py
│   ├── constants
│   │   ├── __init__.py
│   │   └── constants.py
│   ├── controllers
│   │   ├── __init__.py
│   │   ├── user
│   │   │   ├── __init__.py
│   │   │   └── router.py
│   ├── db
│   │   ├── __init__.py
│   │   ├── base.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── user.py
│   ├── middlewares
│   │   ├── __init__.py
│   │   └── rolebase_middleware.py
```

## DB Migration Run Guides

### Prerequisites
- Ensure PostgreSQL is installed and running
- Make sure all dependencies are installed via `pip install -r requirements.txt`
- Configure database connection in `.env` file

### Initial Setup
1. Initialize Alembic:

```bash
alembic init alembic
```
2. Create the initial migration:
```bash
alembic revision --autogenerate -m "initial migration"
```
3. Apply the migration:
```bash
alembic upgrade head
```
### Adding New Migrations
1. Create a new migration:
```bash
alembic revision --autogenerate -m "new migration"
```
2. Apply the migration:
```bash
alembic upgrade head
```
### Rolling Back Migrations
1. Rollback the last migration:
```bash
alembic downgrade -1
```
2. Rollback to a specific migration:
```bash
alembic downgrade <migration_id>
``` 
## Run Seed Data
```bash
python seed_data.py
```
