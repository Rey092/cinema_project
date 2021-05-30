FROM python:3.9

ENV PYTHONPATH /usr/src/app

RUN mkdir -p $PYTHONPATH
RUN mkdir -p $PYTHONPATH/static

# where the code lives
WORKDIR $PYTHONPATH

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install app and dependencies
COPY . $PYTHONPATH
RUN pip install --upgrade pip
COPY ./requirements.txt $PYTHONPATH
RUN pip install -r requirements.txt

# collectstatic
RUN ["python", "src/manage.py", "collectstatic"]

# make entrypoint
COPY ./entrypoint.sh .
RUN ["chmod", "+x", "/usr/src/app/entrypoint.sh"]
ENTRYPOINT ["sh", "/usr/src/app/entrypoint.sh"]
