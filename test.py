import requests

r = requests.post('http://localhost:5000/register', json={'username': 'suke', 'email':'rabin.adk1@gmail.com', 'password':'testing', 'counterid':1})
# r = requests.get('http://localhost:5000/api')
