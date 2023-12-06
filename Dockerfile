ARG BASE_IMAGE=python:3.11-alpine

FROM ${BASE_IMAGE} AS builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV POETRY_VENV=/poetry_venv
RUN python3 -m venv $POETRY_VENV

ENV VIRTUAL_ENV=/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apk update && apk add --no-cache \
        g++ \
        curl \
        git \
        libffi-dev \
        openssl-dev \
        musl-dev


WORKDIR /workspace

COPY pyproject.toml poetry.lock ./
RUN $POETRY_VENV/bin/pip install -U pip poetry && \
        $POETRY_VENV/bin/poetry install --without dev

FROM ${BASE_IMAGE} AS base
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV POETRY_VENV=/poetry_venv
RUN python3 -m venv $POETRY_VENV

ENV VIRTUAL_ENV=/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN $POETRY_VENV/bin/pip install -U pip

COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV
COPY ./pdbrc.py /root/.pdbrc.py

WORKDIR /workspace

FROM base AS final

COPY . /workspace
ENTRYPOINT ["redbot"]


FROM base AS dev
RUN apk update && apk add --no-cache \
        g++ \
        libffi-dev \
        musl-dev
COPY . /workspace
RUN $POETRY_VENV/bin/pip install -U pip poetry && $POETRY_VENV/bin/poetry install
ENTRYPOINT ["redbot"]
