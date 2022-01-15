FROM --platform=linux/amd64 tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

WORKDIR /app

ENV PIP_NO_CACHE_DIR=1

RUN pip install poetry && poetry config virtualenvs.create false

COPY ./pyproject.toml /app/
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install ; else poetry install --no-dev ; fi"
RUN pip install uvicorn

#COPY ./app /app
COPY . /app

#CMD [ "/app/start.sh"]
CMD ["/start-reload.sh"]