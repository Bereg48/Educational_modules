FROM python:3.10-slim

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY ./requirements.txt /code/

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
#CMD ["python", "manage.py", "migrate"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]