# Importa a função 'get' da biblioteca 'requests' para fazer requisições HTTP.
from requests import get

def getBrazilStates():
    # Inicializa um dicionário vazio para armazenar os estados (ex: {'SP': 'São Paulo'}).
    states = {}
    # Faz uma requisição GET para a API que retorna a lista de UFs do IBGE.
    response = get("https://brasilapi.com.br/api/ibge/uf/v1")
    # Itera sobre cada item (cada estado) na resposta JSON da API.
    for e in response.json():
        # Adiciona o estado ao dicionário, usando a sigla como chave e o nome como valor.
        states[e['sigla']] = e['nome']
    return states


# Define uma função para formatar a lista de estados para ser usada em um formulário (especificamente para um WTForms SelectField).
def getStatesAtTuple():
    # Chama a função anterior para obter o dicionário de estados.
    states = getBrazilStates()
    # Inicializa uma lista vazia que irá conter as tuplas no formato (valor, texto_exibido).
    allStates = list()
    # Adiciona uma opção padrão/placeholder para o campo de seleção do formulário.
    allStates.append(("", "Escolha um Estado"))
    # Itera sobre os pares de chave (uf) e valor (name) do dicionário de estados.
    for uf, name in states.items():
        # Itera sobre os pares de chave (uf) e valor (name) do dicionário de estados.
        # Ex: ('sp', 'São Paulo')
        allStates.append((uf.lower(), name))

    return allStates