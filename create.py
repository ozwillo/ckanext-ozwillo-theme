import requests

API='24365b05-a5f2-44ae-a6c6-4379bfd44334'
URL= 'http://ckan-dev:5000/api/3/action/group_create'

data = {
	'name': 'ddd',
	'state':'active'
}

headers = {
    'Authorization': API
}

requests.post(URL, json=data, headers=headers)
