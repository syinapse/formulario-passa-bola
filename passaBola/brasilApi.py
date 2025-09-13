import requests


def getBrazilStates():
    states = {}
    response = requests.get("https://brasilapi.com.br/api/ibge/uf/v1")
    for e in response.json():
        states[e['sigla']] = e['nome']
    return states

def getStatesAtTuple():
    states = getBrazilStates()
    allStates = list()
 #   allStates.append(("", "Escolha uma Cidade"))
    for uf, name in states.items():
        allStates.append((uf, name))
    return allStates