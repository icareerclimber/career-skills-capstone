from flask import Flask, request, send_from_directory, render_template
#from flask_cors import CORS

app = Flask(__name__, static_url_path='')
#CORS(app)

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/MockResponse')
def send_mock_response():
     return "Your next three steps in career are manager, director, and ceo."



if __name__ == "__main__":
    app.run()
