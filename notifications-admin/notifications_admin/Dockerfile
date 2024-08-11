FROM python:3.12-slim as python-base

    # python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    POETRY_VERSION=1.8.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"


ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential

RUN --mount=type=cache,target=/root/.cache \
    curl -sSL https://install.python-poetry.org | python3 -

WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

RUN --mount=type=cache,target=/root/.cache \
    poetry install --without=dev


FROM python-base as production
ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH


WORKDIR /opt/app

COPY ./notifications_admin/entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

COPY ./notifications_admin/uwsgi/uwsgi.ini uwsgi.ini
COPY ./notifications_admin/ .


