import requests
import urllib
import json

database_url = "https://news-banco.centeias.net/retrieve"

def database_availability():
    import ssl
    
    context = ssl._create_unverified_context()
    url = urllib.request.urlopen(database_url, context=context)
    data = json.loads(url.read().decode())
    return data




print(database_availability())

# import urllib.request
# import ssl

# ssl.match_hostname = lambda cert, hostname: True

# request_url = ("https://news-banco.centeias.net/retrieve")
# api_data = urllib.request.urlopen(request_url)
# print(api_data)