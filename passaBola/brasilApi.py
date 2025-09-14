from requests import get

def getBrazilStates():
    states = {}
    response = get("https://brasilapi.com.br/api/ibge/uf/v1")
    for e in response.json():
        states[e['sigla']] = e['nome']
    return states

def getStatesAtTuple():
    states = getBrazilStates()
    allStates = list()
    allStates.append(("", "Escolha um Estado"))
    for uf, name in states.items():
        allStates.append((uf.lower(), name))
    return allStates