FROM python:slim

RUN apt-get update && apt-get install git -y

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app
RUN pip install octohatrack

ENTRYPOINT ["python", "octohatrack.py"]
CMD ["-h"]

