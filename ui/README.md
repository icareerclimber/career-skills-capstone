To try UI on localost, simply

```
cd to current directory
python -m SimpleHTTPServer 8000

Then open brower to http://localhost:8000.
```

To use flask server

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
