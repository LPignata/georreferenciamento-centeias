from flask import render_template, Flask, jsonify, url_for, request
import requests
import json
import datetime
import logging
import os
from pprint import pprint
from db_request import retrieve_json, process_json, available_diseases
from waitress import serve
    
logging.basicConfig(filename='static/entries.log', level=logging.ERROR)

app = Flask(__name__, static_url_path='/static')

database_url = "https://news-banco.centeias.net/retrieve?"
# database_url = 'https://sala-de-situacao-bd.herokuapp.com/retrieve?'

# parametros de filtragem
params_dict = {'disease': '', 'globe': '', 'data_begin': '', 'data_end': ''}

@app.route("/access/dates")
# Retorna quantos acessos cada data teve
def get_dates():
    print('asking for number of access by date')
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
    print('asking for number of access by ips')
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
    data = available_diseases(database_url)
    if data == None:
        return {}
    else:
        return jsonify(data)

@app.route('/get_database_search')
def get_database_search():
    print('A search has been requested')
    # Prepara a query a ser enviada para o banco de dados
    global params_dict
    search_query = ''
    date = []
        
    params_dict['disease'] = request.args.get('disease','')
    if(params_dict['disease'] == 'all-diseases'):        
        params_dict['disease'] = ''
    
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
    
    if data == None:
        print('The search parameters returned nothing')
        return jsonify({})

    if(params_dict['disease'] == ''):
        params_dict['disease'] == 'Todas doenças'
    
    print('the search requisition is completed')
    return jsonify(process_json(data, params_dict['globe'] == "countries", date, params_dict['disease']))

# Testa se o banco está disponível
def database_availability():
    print('Testing database availability...')
    request = requests.get(database_url, verify=False)
    print('Database returned http code: ' + str(request.status_code))
    return request.status_code == 200

@app.route('/')
def main_page(name=None):
    print('Home page request')
    # Caso o banco não esteja disponível alerte o usuário
    if(database_availability() == False):
        print('Database didn\'t return http 200!')
        return render_template('db_error.html')
    
    print('Database functioning correctly!')

    global params_dict
    logger = logging.getLogger()
    date = datetime.date.today()
    ip   = request.environ['REMOTE_ADDR']

    print('logged ip')

    logger.error(str(ip) + ' ' + str(date))
    
    params_dict['disease'] = request.args.get('disease','')
    params_dict['globe'] = request.args.get('globe','')
    params_dict['data_begin'] = request.args.get('data_begin','')    
    params_dict['data_end'] = request.args.get('data_end','')        

    print('Returning home page html')
    return render_template('index.html')

if __name__ == "__main__":    
    print('Starting app...')
    # app.run(port=3000, debug=True)    
    serve(app, port=5000)