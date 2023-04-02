# pull official base image
FROM python:3.9.6-alpine

# set work directory
WORKDIR /usr/src/app


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
RUN pip install requests
RUN pip install aiogram
RUN pip install django

# copy project
COPY . .

CMD [ "python", "./telegram.py" ]


