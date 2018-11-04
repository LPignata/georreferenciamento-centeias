from flask import render_template, Flask, jsonify, url_for
import requests
import json

app = Flask(__name__, static_url_path='/static')

@app.route('/retrieve_estates')
def retrieve_estates():
    with open('static/estates.json') as f:
        data = json.load(f)
    return(jsonify(data))

@app.route('/retrieve_news')
def retrieve_news():
    url = 'https://sala-de-situacao-bd.herokuapp.com/retrieve'
    r = requests.get(url)
    j = r.json()    
    return (jsonify(j))

@app.route('/')
def hello(name=None):
    return render_template('index.html')

app.run(debug = True, port = 80)    