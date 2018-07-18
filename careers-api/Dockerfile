FROM python:3.6

ADD . /careers-api
WORKDIR /careers-api

RUN pip install -r requirements.txt
RUN python -m nltk.downloader stopwords
ENV FLASK_APP server.py

ENTRYPOINT ["python"]
CMD ["-m", "flask", "run", "--host=0.0.0.0"]

EXPOSE 5000
