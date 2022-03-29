FROM python:3.9.7

WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV ENVIRONMENT dev
ENV TESTING 0
ENV DATABASE_HOSTNAME=localhost
ENV DATABASE_PORT=5432
ENV DATABASE_PASSWORD=Expires21!!
ENV DATABASE_NAME=poi_api_db
ENV DATABASE_USERNAME=postgres
ENV SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
ENV ALGORITHM=HS256
ENV ACCESS_TOKEN_EXPIRE_MINUTES=30
ENV DATABASE_URL=postgresql://postgres:Expires21!!@localhost:5432/poi_api_db

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--port", "8000" ]
