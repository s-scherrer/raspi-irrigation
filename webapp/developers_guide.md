# Developer's guide for irrigation webapp

## Dependencies & Environments

For local developping and testing I use the conda environment defined in
`environment.yml`. This installs run-time requirements, which should go into
`requirements.txt`, and development requirements (only in `environment.yml`,
e.g. `pytest`).

To create the conda environment, run
```
conda env create -f environment.yml
```

For production, the app is deployed as docker container. Here, only
`requirements.txt` are installed. To build the container, do
```
sudo docker build -t irrigation_webapp .
```
Normally, this will be done by `docker-compose` in the top level directory,
this is only required if you want to test out the single container.
