FROM python:3.10.9

# Path: /app
RUN mkdir /app

# change workdir
WORKDIR /app

# copy requirements.txt to /app
COPY requirements.txt .

# install requirements.txt
RUN pip install -r requirements.txt

# copy all files to /app
COPY . .

# RUN chmod a+x *.sh

# run the alembic migrations
RUN alembic upgrade head

# run app
CMD gunicorn src.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000