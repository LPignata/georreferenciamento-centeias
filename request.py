import urllib.request, json 
from pprint import pprint

query_url = 'https://sala-de-situacao-bd.herokuapp.com/retrieve?'

def retrieve_json(this_url):
    with urllib.request.urlopen(this_url) as url:
        data = json.loads(url.read().decode())
        # Query vazia
        if(data == []):            
            return {}        
        else:    
            return data
    
def process_json(data, seach_globe):
    dic = {}    

    for result in data:
        if seach_globe:
            # Se o resultado for global pesquise paises
            local = result['country']
        else:
            # se n, pesquise estados
            local = result['region']    

        if local == '':
            continue
        if (local not in dic):
            dic[local] = 1
        else:
            dic[local] += 1    

    result_dictionary = {}

    result_dictionary['globe'] = seach_globe
    result_dictionary['data'] = []    
    for d in dic:        
        result_dictionary['data'].append({'local': d, 'count': dic[d]})
        
    pprint(result_dictionary)

# process_json(retrieve_json(query_url + 'content=Teve'), True)