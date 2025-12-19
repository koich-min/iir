FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN set -eux; \
  apt-get update; \
  apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    libpq-dev \
    default-libmysqlclient-dev \
    ca-certificates \
    curl; \
  rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY . /app

RUN pip install --upgrade pip \
  && pip install --no-cache-dir ".[postgres]"


ARG DJANGO_SECRET_KEY=build-time-only
ENV DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY

RUN python manage.py collectstatic --noinput

RUN groupadd --system iir && useradd --system --gid iir --create-home iir \
  && chown -R iir:iir /app

USER iir
