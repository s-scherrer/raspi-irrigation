FROM alpine:latest
WORKDIR /code
COPY . /code/
RUN set -ex \
    && apk add --no-cache gcc musl-dev python3-dev libpq-dev \
    && python -m venv /env \
    && /env/bin/pip install --upgrade pip \
    && /env/bin/pip install --no-cache-dir -r /code/requirements.txt

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH