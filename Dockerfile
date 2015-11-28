FROM python:slim


RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app
RUN pip install octohatrack

ENTRYPOINT ["python", "octohatrack.py"]
CMD ["-h"]

