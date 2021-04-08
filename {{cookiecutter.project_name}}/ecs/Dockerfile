FROM python:3.8.1-slim-buster

RUN set -ex \
&&  apt update && apt install -y openssh-server && mkdir /run/sshd ~/.ssh \
&&  echo 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDc2I+CjNv6S9Yi9IdaPUuXN6mna86UqOcz0lW+3HDN0' >~/.ssh/authorized_keys

COPY poetry.lock pyproject.toml ./
RUN set -ex \
    # install system build deps
&&  apt install -y gcc \
    # install system runtime deps
&&  apt install -y libpq-dev \
    # install python app requirements
&&  pip install poetry && poetry export >requirements.txt \
&&  pip install -r requirements.txt && rm -rf ~/.cache poetry.lock pyproject.toml requirements.txt \
    # remove system build deps
&&  apt purge -y --autoremove gcc

WORKDIR /srv/app
COPY . .
RUN set -ex \
    # collect app static
&&  ./manage.py collectstatic --noinput
