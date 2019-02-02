import requests

r = requests.post('http://localhost:5000/register', json={'username': 'maverick', 'email':'rabin.adk1@gmail.com', 'password':'testing', 'counterid':1})
