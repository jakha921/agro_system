# Fastapi + Alembic + SQLAlchemy + PostgreSQL + Async

## Description

This is a template for a FastAPI project with Alembic migrations, SQLAlchemy ORM, PostgreSQL database and async support.

---

## Requirements

if you are using [venv](https://docs.python.org/3/library/venv.html)
or [virtualenv](https://virtualenv.pypa.io/en/latest/) you can install the requirements with the following command:

```bash
python3 -m venv <name_of_your_venv>
```

in **Unix** systems: ```bash source <name_of_your_venv>/bin/activate ```

in **Windows** systems: ```bash <name_of_your_venv>\Scripts\activate.bat ```

then:

```bash
pip install -r requirements.txt
```

---

## Usage

### .env file

Create a .env file in the root of the project with the following variables:

```bash
DB_HOST=localhost # or your host <ip> or <domain>
DB_PORT=5432  # or your port
DB_NAME=postgres # or your database name 
DB_USER=postgres # or your user
DB_PASS=postgres # or your password
```

### In models.py

Change the name of the model to the name of your table and the name of the columns to the name of your columns.

#### To create a migration

```bash
alembic revision --autogenerate -m "migration name"
```

#### To apply a migration

```bash
alembic upgrade head
```

---

### Run the app

```bash
uvicorn src.main:app --reload
```
