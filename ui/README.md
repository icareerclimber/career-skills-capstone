To try UI on localost, simply

```
cd to current directory
python -m SimpleHTTPServer 8000

Then open brower to http://localhost:8000.
```

To build container and try locally

```
cd ui directory
docker build -t flask-ui:0.1 -f Dockerfile.3.6 .
docker run -it --net=host flask-ui:0.1

Then point web browser to localhost:5000 (127.0.0.1 does not work)
```

To use flask server on local machine:

export FLASK_APP=server.py
export FLASK_ENV=development

flask run

templates/index.html is used for render_template
static/index.js and style.css is used for send_static_file
## Docker instructions:
### Requirements
Have the following installed in your local environment:

- docker
  - https://docs.docker.com/install/
- docker-compose
  - https://docs.docker.com/compose/install/

### Instructions
From the ui root directory run:
```
docker-compose up -d
```
To force a rebuild of the container:
```
docker-compose up -d --build
```

#### Verify installation

Check that the application is working by navigating in the browser to `localhost:8000`

#### To stop the application
From the resume-assistant root direction run:
```
docker-compose down
```
