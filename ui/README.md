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
