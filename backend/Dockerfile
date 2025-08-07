FROM python:3.10.12 as builder

# keeps python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1
# application directory
ENV APP_DIR /app
# set work directory
WORKDIR ${APP_DIR}

COPY requirements.txt .

RUN apt-get update && apt-get install -y gettext
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

EXPOSE 8000