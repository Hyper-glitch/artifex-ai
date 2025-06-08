FROM python:3.11.4-slim

LABEL org.opencontainers.image.authors="smirnov.roman.olegovich@gmail.com"
ARG requirements_file="/opt/app/requirements.txt"

RUN apt-get update -y --fix-missing \
    && apt-get install -y libffi-dev libc6-dev libpq-dev libssl-dev --no-install-recommends \
    && apt-get -y clean

WORKDIR /opt/app

COPY ./pyproject.toml ./poetry.lock ./
RUN pip install poetry==1.6.1  \
    && poetry export -f requirements.txt > $requirements_file  --without-hashes --without linters,typing  \
    && pip install -r $requirements_file

COPY . /opt/app

WORKDIR /opt/app
ENV PYTHONPATH="/opt/app"

CMD ["python", "-m", "src.bot"]
