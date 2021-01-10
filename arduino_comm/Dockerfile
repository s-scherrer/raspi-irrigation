FROM continuumio/miniconda3
WORKDIR /code
COPY . /code/
RUN conda install -y --file /code/requirements.txt
CMD ["/opt/conda/bin/python", "/code/run_arduino_comm.py"]