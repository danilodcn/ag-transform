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

RUN apt update && apt install libpq-dev gcc make libjpeg-dev curl git -y

RUN apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -U pip && pip install poetry

RUN useradd -ms /bin/bash python
USER python
WORKDIR /home/python/app/
COPY pyproject.toml poetry.lock /home/python/app/

USER root
RUN poetry config virtualenvs.create false \
    # && poetry install --no-dev --no-interaction --no-ansi
    && poetry install $(/usr/bin/test "$DEV_ENV" == "production" && echo "--no-dev")

USER python
RUN poetry config virtualenvs.create false

COPY . .

CMD ["tail", "-f", "/dev/null"]
# CMD [ "sh", "./src/internal_scripts/web.sh" ]
