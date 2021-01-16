FROM continuumio/miniconda3:4.9.2
WORKDIR /code
COPY . /code/
RUN conda env update -n base -f /code/environment.yml
ENTRYPOINT python run_arduino_comm.py