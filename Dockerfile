FROM python:3.9.0

WORKDIR /home/

RUN echo "testing 2240"

RUN git clone https://github.com/shong91/MovieLiker.git

WORKDIR /home/MovieLiker/

RUN pip install -r requirements.txt

RUN pip install gunicorn

RUN pip install mysqlclient

EXPOSE 8000

CMD ["bash", "-c", "python manage.py migrate --settings=MovieLiker.settings.deploy && gunicorn MovieLiker.wsgi --env DJANGO_SETTINGS_MODULE=MovieLiker.settings.deploy --bind 0.0.0.0:8000"]
