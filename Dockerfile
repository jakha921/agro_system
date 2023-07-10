FROM python:3.10

# Path: /app
RUN mkdir /app

# change workdir
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy all files to /app
COPY . .

RUN chmod a+x *.sh

# run the alembic migrations
RUN alembic upgrade head

# run app
CMD gunicorn src.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
