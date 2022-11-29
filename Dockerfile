FROM --platform=linux/amd64 tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

WORKDIR /app

ENV PIP_NO_CACHE_DIR=1

RUN pip install poetry && poetry config virtualenvs.create false

RUN apt update
RUN apt install git -y

COPY ./pyproject.toml /app/
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install ; else poetry install --no-dev ; fi"
RUN pip install uvicorn

RUN mkdir /app/pipelines

COPY . /app

CMD ["/start-reload.sh"]