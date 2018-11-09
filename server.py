from flask import render_template, Flask, jsonify, url_for, request
import requests
import json
import datetime
import logging
    
logging.basicConfig(filename='static/error.log', level=logging.ERROR)

app = Flask(__name__, static_url_path='/static')

@app.route("/dates")
def get_dates():
    with open('static/error.log') as my_file:
        lines = my_file.readlines()

    dic = {}
    for line in lines:
        line = line.replace('ERROR:root:','')
        arr  = line.split(' ')        
        date = arr[1]
        if date not in dic:
            dic[date] = 0            
        dic[date] += 1

    return jsonify(dic)

@app.route("/ips")
def get_ips():
    with open('static/error.log') as my_file:
        lines = my_file.readlines()

    dic = {}
    for line in lines:
        line = line.replace('ERROR:root:','')
        arr  = line.split(' ')        
        ip = arr[0]
        if ip not in dic:
            dic[ip] = 0            
        dic[ip] += 1

    return jsonify(dic)    

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
    logger = logging.getLogger()
    date = datetime.date.today()
    ip   = request.environ['REMOTE_ADDR']

    logger.error(str(ip) + ' ' + str(date))

    return render_template('index.html')

if __name__ == '__main__':    

    app.run(host='0.0.0.0', debug = True, port = 8080)
