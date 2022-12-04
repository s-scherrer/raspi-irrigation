FROM alpine:latest
WORKDIR /code
COPY . /code/
ADD ./requirements.txt /code/requirements.txt
RUN set -ex \
    && apk update \
    && apk add --no-cache gcc musl-dev python3-dev libpq-dev \
    && python -m venv /env \
    && /env/bin/pip install --upgrade pip \
    && /env/bin/pip install --no-cache-dir -r /code/requirements.txt

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH