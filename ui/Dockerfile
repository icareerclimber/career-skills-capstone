FROM python:3.6

ADD . /ui
WORKDIR /ui

RUN pip install -r requirements.txt
ENV FLASK_APP server.py

ENTRYPOINT ["python"]
CMD ["-m", "flask", "run", "--host=0.0.0.0", "--port=8081"]

EXPOSE 5000
