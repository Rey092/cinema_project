FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUNBUFFERED 1

WORKDIR /usr/src/cinema_project

COPY ./requirements.txt /usr/src/requirements.txt
RUN pip install -r /usr/src/requirements.txt

COPY . /usr/src/cinema_project

EXPOSE 8001
CMD ['make', 'run']
