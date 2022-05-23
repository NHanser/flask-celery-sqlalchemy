# Our docker-compose file uses Dockerfile-dev instead of Dockerfile

FROM python:3.10-slim as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base as python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apt update && apt install -y gcc python3-dev

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base as runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Create and switch to a new user
#RUN useradd --create-home appuser
#WORKDIR /home/appuser
#USER appuser


# Install application into container
COPY . /myapp

WORKDIR /myapp

RUN chmod +x /myapp/gunicorn.sh
ENV APP_RUN_ENV=DOCKER
EXPOSE 5000