import requests
from model import ClienteModel

API_URL = "http://127.0.0.1:5000/"
ENDPOINT_GET = API_URL + "clientes"

def get_all(page=None, limit=None):
    if not page or not limit:
        URL = ENDPOINT_GET
    else:
        URL = f"{ENDPOINT_GET}?page={page}&limit={limit}"
    dict_response = requests.get(URL).json()
    dict_response["clientes"] = [ClienteModel(**c)
                                 for c in dict_response["clientes"]]
    return dict_response

def get(conta):
    URL = ENDPOINT_GET + "/" + str(conta)
    dict_response = requests.get(URL).json()
    return ClienteModel(**dict_response)

def post(cliente):
    requests.post(ENDPOINT_GET, data=cliente.to_dict())

def put(cliente):
    URL = ENDPOINT_GET + '/' + str(cliente.conta)
    requests.put(URL, data=cliente.to_dict())

def delete(conta):
    URL = ENDPOINT_GET + '/' + str(conta)
    requests.delete(URL)