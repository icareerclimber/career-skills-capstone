from flask import Flask, request, send_from_directory, render_template

import urllib3
import urllib.parse
import json

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

@app.route('/postSummary')
def returnMatches():
     http = urllib3.PoolManager()
     #data = {"experience":[{"title": "software engineeer", "description": "i build data models"}]}
     print(request.headers)
     title = request.headers.get('x-career-climber-lastTitle')
     description = urllib.parse.unquote(request.headers.get('x-career-climber-lastDescription'))
     data = {"experience":[{"title": title, "description": description}]}
     #data = {"experience":[{"title": "manager", "description": "manage a lot of people"}]}
     # instrument for local test
     try:
       r = http.request(
         "POST", "http://icareers-api:5000/model/similar_jobs",
         body=json.dumps(data),
         headers={'Content-Type': 'application/json'})
     except:
       r = http.request(
         "POST", "http://127.0.0.1:5000/model/similar_jobs",
         body=json.dumps(data),
         headers={'Content-Type': 'application/json'})

     rJson = json.loads(r.data.decode('utf-8'))
     for i in rJson['results']:
        print(i)
     result = ''
     c = 0
     for i in rJson['results']:
         if result == '':
           #result = '<ul><li k=' + urllib.parse.quote(i['title']) + '>title: ' + i['title'] + ', probability: ' + str(i['probability']) + '</li>'
           result = '<ul id="similarJobs"><li k=' + \
                urllib.parse.quote(i['title']) + \
                '>' + \
                '<a class="similarJob" href="#startSkillSet" onClick=getSkillSet(\'' + urllib.parse.quote(i['title']) + '\'); return false>'  + \
                i['title'] + \
                '</a>' + \
                '{:.1%}'.format(i['probability']) + ' similar, </li>'
         else:
           result = result + '<li k=' + \
                urllib.parse.quote(i['title']) + \
                '>' + \
                '<a class="similarJob" href="#startSkillSet" onClick=getSkillSet(\'' + urllib.parse.quote(i['title']) + '\'); return false;>'  + \
                i['title'] + \
                '</a>' + \
                '{:.1%}'.format(i['probability']) + ' similar, </li>'

         c = c + 1
         if c > 10:
           break
     result = result + '</ul>'

     return result 

@app.route('/getSkillSet')
def returnSkillSet():
     http = urllib3.PoolManager()
     title = request.headers.get('x-career-climber-lastTitle')
     try:
       r = http.request(
         "GET", "http://icareers-api:5000/model/skills/" + title)
     except:
       r = http.request(
         "GET", "http://127.0.0.1:5000/model/skills/" + title)
     rJson = json.loads(r.data.decode('utf-8'))
     result = ''
     c = 0
     for i in rJson['results']:
         if result == '':
           result = '<h3>Skill Set for <font color="blue">' + urllib.parse.unquote(title) +'</font></h3><ul><li k=' + i + '>' + i + '</li>'
         else:
           result = result + '<li k=' + i + '>' + i + '</li>'
         c = c + 1
         if c > 10:
           break
     result = result + '</ul>'
           
     return result 

if __name__ == "__main__":
    app.run()
else:
    app.run()
