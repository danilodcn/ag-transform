FROM python:3.10.5-slim-buster


ARG DEV_ENV

ENV \
    DEV_ENV=${DEV_ENV} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

RUN apt update \
    && apt install libpq-dev gcc make libjpeg-dev curl git -y \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -U pip && pip install poetry

RUN useradd -ms /bin/bash python

USER python

WORKDIR /home/python/app/

COPY pyproject.toml poetry.lock /home/python/app/

RUN poetry config virtualenvs.in-project true \
    && poetry install

COPY . .

CMD ["tail", "-f", "/dev/null"]
