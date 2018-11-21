from flask import render_template, Flask, jsonify, url_for, request
import requests
import json
import datetime
import logging
import os
from db_request import retrieve_json, process_json, available_diseases
from waitress import serve
    
logging.basicConfig(filename='static/entries.log', level=logging.ERROR)

app = Flask(__name__, static_url_path='/static')

database_url = 'https://sala-de-situacao-bd.herokuapp.com/retrieve?'

# parametros de filtragem
params_dict = {'disease': '', 'globe': '', 'data_begin': '', 'data_end': ''}

@app.route("/access/dates")
# Retorna quantos acessos cada data teve
def get_dates():
    with open('static/entries.log') as my_file:
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
    with open('static/entries.log') as my_file:
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


@app.route('/get_database_diseases')
def get_database_diseases():
    return jsonify(available_diseases(database_url))

@app.route('/get_database_search')
def get_database_search():
    # Prepara a query a ser enviada para o banco de dados
    global params_dict
    search_query = ''
    params_dict['disease'] = request.args.get('disease','')
    params_dict['globe'] = request.args.get('globe','')
    params_dict['data_begin'] = request.args.get('data_begin','')    
    params_dict['data_end'] = request.args.get('data_end','')    
    for parameter in params_dict:        
        if(params_dict[parameter] != ''):
            if('data' in parameter):
                date = params_dict[parameter]
                date = date.split('-')
                search_query += 'year=' + date[0] + '&'
                search_query += 'month=' + date[1] + '&'
                search_query += 'day=' + date[2] + '&'            
            else:
                search_query += parameter + '=' + params_dict[parameter] + '&'
    search_query = search_query[:-1]
    data = retrieve_json(database_url + search_query)
    # return jsonify(data)
    return jsonify(process_json(data, params_dict['globe'] == "countries", date))
    

@app.route('/')
def hello(name=None):    
    global params_dict
    logger = logging.getLogger()
    date = datetime.date.today()
    ip   = request.environ['REMOTE_ADDR']

    logger.error(str(ip) + ' ' + str(date))
    
    params_dict['disease'] = request.args.get('disease','')
    params_dict['globe'] = request.args.get('globe','')
    params_dict['data_begin'] = request.args.get('data_begin','')    
    params_dict['data_end'] = request.args.get('data_end','')    

    return render_template('index.html')

# if __name__ == '__main__':    
#     port = int(os.environ.get("PORT", 80))
#     app.run(host='0.0.0.0',port=port)
serve(app, port=5000)