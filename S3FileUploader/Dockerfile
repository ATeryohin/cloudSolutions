FROM ubuntu:16.04

RUN apt-get update && apt-get install -y software-properties-common vim
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update -y

RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv && \
        apt-get install -y git

# update pip
RUN python3.6 -m pip install pip --upgrade && \
        python3.6 -m pip install wheel

RUN mkdir /python_apps
COPY ./requirements /python_apps/
RUN python3.6 -m pip install -r /python_apps/requirements


COPY ./app/ /python_apps/app/
RUN mkdir /python_apps/tmp/
COPY ./run.py /python_apps/

EXPOSE 8090

ENTRYPOINT ["python3.6", "/python_apps/run.py"]