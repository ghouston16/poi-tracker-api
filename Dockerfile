FROM python:3.9.7

WORKDIR /usr/src/app

# create the app user
RUN addgroup --system app && adduser --system --group app

ENV APP_HOME=/usr/src/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV ENVIRONMENT prod
ENV TESTING 0

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

# run gunicorn
CMD release.sh