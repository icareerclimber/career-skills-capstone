# Use the official go docker image built on debian.
FROM golang:1.10.2

# Add the app code to the container
ADD . /go/src/github.com/resume-assistant

# Install revel and the revel CLI.
RUN go get github.com/revel/revel
RUN go get github.com/revel/cmd/revel

# Run the application
ENTRYPOINT revel run github.com/resume-assistant dev 8080

# Open up the port where the app is running.
EXPOSE 8080
