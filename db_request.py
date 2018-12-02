import urllib.request, json 
from pprint import pprint

def retrieve_json(this_url):
    # Pega um Json do banco de dados
    with urllib.request.urlopen(this_url) as url:
        data = json.loads(url.read().decode())
        # Query vazia
        if(data == []):            
            return None
        else:    
            return data

# Retorna as doencas disponiveis no banco
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

# Processa um Json para o front receber o dado
# search_globe define se deve-se buscar no brasil ou no mundo inteiro
def process_json(data, search_globe, date, disease):
    # count_dic contém quantas noticias tem em cada localização
    count_dic = {}
    # url_dic contém as url's de cada localização
    url_dic = {}

    for result in data:
        if search_globe:
            # Se o resultado for global pesquise paises
            local = result['country']
        else:
            # se n, pesquise estados
            local = result['region']    


        if date != []:
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

        # Inserção dos counts
        if (local not in count_dic):
            count_dic[local] = 1                        
        else:
            count_dic[local] += 1

        # Inserção das urls
        if(local not in url_dic):
            url_dic[local] = [
                {'link': result['url'],
                'title': result['title'],
                'description':result['description']
                }]
        else:
            url_dic[local].append(
                {'link': result['url'],
                'title': result['title'],
                'description':result['description']
                })
                
    result_dictionary = {}

    result_dictionary['globe'] = search_globe
    result_dictionary['disease'] = disease
    result_dictionary['data'] = []    
    
    for d in count_dic:
        result_dictionary['data'].append(
            {
            'local': d,
            'count': count_dic[d],
            'url': url_dic[d]
            })
                
    return result_dictionary