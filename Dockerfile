FROM amazonlinux:2023

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN yum update -y && yum install -y python3-pip

WORKDIR /mysite

COPY requirements.txt /mysite/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /mysite/

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000
