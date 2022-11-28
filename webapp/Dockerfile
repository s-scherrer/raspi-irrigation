FROM continuumio/miniconda3:4.12.0
WORKDIR /code
COPY . /code/
RUN conda env update -n base -f /code/environment.yml
ENTRYPOINT ["/bin/bash", "./docker-entrypoint.sh"]
