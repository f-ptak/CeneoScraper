import requests

url = "https://www.ceneo.pl/65035783#tab=reviews"
response = requests.get(url)
print(response.text)