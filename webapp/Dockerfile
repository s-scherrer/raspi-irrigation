FROM python:3.8
WORKDIR /code
COPY . /code/
RUN pip install -r /code/requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py loaddata observables
CMD python manage.py runserver 0.0.0.0:8000