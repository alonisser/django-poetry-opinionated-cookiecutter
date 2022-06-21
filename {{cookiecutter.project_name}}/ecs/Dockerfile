FROM python:3.9-slim-bullseye

RUN set -ex \
&&  apt update && apt install -y openssh-server && mkdir /run/sshd ~/.ssh

COPY poetry.lock pyproject.toml ./
RUN set -ex \
    # install system build deps
&&  apt install -y gcc \
    # install system runtime deps
&&  apt install -y libpq-dev \
    # install python app requirements
&&  pip install poetry

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

RUN rm -rf ~/.cache poetry.lock pyproject.toml \
    # remove system build deps
  &&  apt purge -y --autoremove gcc

WORKDIR /srv/app
COPY . .
RUN set -ex \
    # collect app static
&&  ./manage.py collectstatic --noinput
