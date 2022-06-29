# Our docker-compose file uses Dockerfile-dev instead of Dockerfile

FROM python:3.10-slim as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONFAULTHANDLER 1

ENV FLASK_ENV="docker"
#ENV FLASK_APP=app/__init__.py
#ENV APP_RUN_ENV=DOCKER
EXPOSE 5000

FROM base as python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apt update && apt install -y gcc python3-dev

# Install python dependencies in /.venv
COPY ./Pipfile .
COPY ./Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base as runtime
# Install application into container
COPY . /myapp
WORKDIR /myapp
# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

FROM runtime as debug
RUN pip install debugpy
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

RUN flask db upgrade
RUN flask init create-users
CMD python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m flask run -h 0.0.0.0 -p ${FLASK_PORT}

FROM runtime as prod
RUN chmod +x /myapp/gunicorn.sh
RUN flask db upgrade
RUN flask init create-users

CMD /myapp/gunicorn.sh

