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
        $POETRY_VENV/bin/poetry install

COPY . /workspace
RUN pip install -e .


FROM ${BASE_IMAGE} AS base
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV POETRY_VENV=/poetry_venv

ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./pdbrc.py /root/.pdbrc.py

COPY . /workspace
WORKDIR /workspace

COPY --from=builder $POETRY_VENV $POETRY_VENV
COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV
ENTRYPOINT ["redbot"]
