import urllib.request, json 
from pprint import pprint

def retrieve_json(this_url):
    with urllib.request.urlopen(this_url) as url:
        data = json.loads(url.read().decode())
        # Query vazia
        if(data == []):            
            return None      
        else:    
            return data

# Retorna as doenças disponiveis no banco
def available_diseases(url):
    data = retrieve_json(url)
    array = []
    dic = {}
    for result in data:
        disease = result['disease']
        if disease:
            array.append(disease)

    array = (list(set(array)))
    dic['diseases'] = array
    return dic

def process_json(data, seach_globe, date):
    dic = {}    

    for result in data:
        if seach_globe:
            # Se o resultado for global pesquise paises
            local = result['country']
        else:
            # se n, pesquise estados
            local = result['region']    

        date_result = result['date'].split('T')[0].split('-')
        if date_result[0] > date[0]:
            continue
        elif date_result[0] == date[0]:
            if date_result[1] > date[1]:
                continue
            elif date_result[1] == date[1]:
                if date_result[2] > date[2]:
                    continue

        if local == '':
            continue
        if (local not in dic):
            dic[local] = 1
        else:
            dic[local] += 1    

    result_dictionary = {}

    result_dictionary['globe'] = seach_globe
    result_dictionary['disease'] = result['disease']
    result_dictionary['data'] = []    
    for d in dic:        
        result_dictionary['data'].append({'local': d, 'count': dic[d]})
        
    return result_dictionary