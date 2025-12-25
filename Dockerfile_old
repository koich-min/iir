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

ARG IIR_EXTRAS=""
RUN pip install --upgrade pip \
  && pip install --no-cache-dir ".${IIR_EXTRAS}"

RUN groupadd --system iir && useradd --system --gid iir --create-home iir \
  && chown -R iir:iir /app

USER iir
