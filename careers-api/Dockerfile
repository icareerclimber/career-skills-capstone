FROM python:3.6

# Set up FUSE to mount object store
RUN apt-get update && apt-get install --yes lsb-release
RUN apt-get install --yes --no-install-recommends \
    ca-certificates \
    curl \
 && echo "deb http://packages.cloud.google.com/apt gcsfuse-`lsb_release -c -s` main" | tee /etc/apt/sources.list.d/gcsfuse.list \
 && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - \
 && apt-get update \
 && apt-get install --yes gcsfuse \
 && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy app to container
RUN mkdir /mnt/career-capstone
ADD . /careers-api
WORKDIR /careers-api

# Install python dependencies
RUN pip install -r requirements.txt && python -m nltk.downloader stopwords \
  && python -m nltk.downloader punkt && python -m nltk.downloader wordnet
ENV FLASK_APP server.py

# Runn app
ENTRYPOINT ["python"]
CMD ["-m", "flask", "run", "--host=0.0.0.0"]

VOLUME /mnt/career-capstone
EXPOSE 5000
