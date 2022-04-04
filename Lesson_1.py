import requests
import json

url = 'https://api.github.com/users/'

# header={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}

name= input("Введите имя пользователя: ")
rep='/repos'

response=requests.get(url+name+rep)

if response.ok:
    data=json.loads(response.text)
    repositories=[]
    print(f'Ропозитории пользователя {name}:')
    for repos in data:
        print(repos['name'])
else:
    print(f'Ошибка{response.status_code}')

with open(f'{name}_repositories.json','w') as f:
    json.dump(repositories,f)

