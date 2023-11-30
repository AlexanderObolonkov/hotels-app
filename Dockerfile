FROM python:3.11

RUN mkdir /booking

WORKDIR /booking

COPY poetry.lock pyproject.toml ./

# TODO: poetry integration