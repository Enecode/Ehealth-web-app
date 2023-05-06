FROM python:3.8-slim-buster
WORKDIR /code
COPY . /code/
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]