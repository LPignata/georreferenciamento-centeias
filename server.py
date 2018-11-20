from flask import render_template, Flask, jsonify, url_for, request
import requests
import json
import datetime
import logging
import os
    
logging.basicConfig(filename='static/error.log', level=logging.ERROR)

app = Flask(__name__, static_url_path='/static')

@app.route("/access/dates")
# Retorna quantos acessos cada data teve
def get_dates():
    with open('static/error.log') as my_file:
        lines = my_file.readlines()

    dic = {}
    for line in lines:
        line = line.replace('ERROR:root:','')
        arr  = line.split(' ')        
        date = arr[1]
        date = date.rstrip()
        if date not in dic:
            dic[date] = 0            
        dic[date] += 1

    return jsonify(dic), 200

@app.route("/access/ips")
# Retorna quantas vezes cada ip acessou
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

    return jsonify(dic), 200

@app.route('/retrieve_estates')
# Usada internamente
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

@app.route('/api')
def api():
    disease = request.args.get('disease','')
    globe = request.args.get('globe','')
    data_begin = request.args.get('data_begin','')
    data_end = request.args.get('data_end','')
    print(disease)
    return disease

@app.route('/')
def hello(name=None):    
    logger = logging.getLogger()
    date = datetime.date.today()
    ip   = request.environ['REMOTE_ADDR']

    logger.error(str(ip) + ' ' + str(date))

    return render_template('index.html')

if __name__ == '__main__':    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0',port=port)
