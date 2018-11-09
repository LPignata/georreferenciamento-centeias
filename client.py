import requests

r = requests.get('http://127.0.0.1:8080/log')
print(r.content.decode('utf-8'))