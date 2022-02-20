FROM python:3.10.0

LABEL maintainer="fakeemail@fake.fake"
LABEL vendor="HypeKitty"

# Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONHASHSEED random
ENV PYTHONBREAKPOINT ipdb.set_trace

# Pip
ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK on
ENV PIP_DEFAULT_TIMEOUT 100

# Django
ENV DJANGO_SETTINGS_MODULE api.settings
ENV TZ America/Sao_Paulo

# Dependencies
COPY ./requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /usr/src/app
COPY ./src /usr/src/app
