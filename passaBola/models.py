# Importa as bibliotecas necessárias.
from requests import post
from json import dump, load, dumps
from uuid_extensions import uuid7str # Para gerar IDs únicos baseados em tempo.
from wtforms import ValidationError
from passaBola import cpf_api_key # Importa a chave da API do arquivo __init__.py.
from pathlib import Path
from datetime import datetime
database_path = Path("./passaBola/database/database.json")

# Define o caminho para o arquivo JSON que funciona como banco de dados.
def readDatabase():
    with open(database_path, "r") as db:
        data = load(db)
    return data

# Função para validar um CPF e data de nascimento através de uma API externa.
def checkCPF(cpf, birthday):
    url = "https://api.cpfhub.io/api/cpf"
    header = {
        "x-api-key": cpf_api_key,
        "Content-Type": "application/json"

    }
    data = {
        "cpf": cpf,
        "birthDate": birthday
    }

    # Envia a requisição POST para a API e retorna a resposta em formato JSON.
    data = post(url, json=data, headers=header).json()
    return data

# Classe que representa o modelo de dados de uma Jogadora.
class Player():
    # Método construtor para criar uma nova instância de Player.
    def __init__(self, cpf, full_name, birthday, email, phone, state, instagram = None):
        self.id = uuid7str() # Id único aleatório em UUID7
        self.cpf = cpf
        self.full_name = full_name
        self.birthday = birthday
        self.email = email
        self.phone = phone
        self.state = state
        self.instagram = instagram if instagram != None else "INEXISTENTE"

    # Método de classe alternativo para criar uma instância simplificada de Player (usado por um time).
    @classmethod
    def TeamsPlayers(cls, cpf, name):
        return cls(cpf=cpf, full_name=name, birthday=None, email=None, phone=None, state=None)

    # Método estático para ler e retornar apenas a lista de jogadoras do banco de dados.
    @staticmethod
    def readPlayers():
        with open(database_path, "r") as pl:
            data = load(pl)
        return data["players"]
    
    # Método para escrever a instância atual da jogadora no banco de dados.
    def witeNewPlayer(self):
        db = readDatabase() # Lê o banco de dados inteiro.
        newPlayer = self.__dict__  # Converte o objeto Player para um dicionário.
        newPlayer['birthday'] = newPlayer['birthday'].strftime("%d-%m-%Y") # Formata a data.
        db['players'].append(newPlayer) # Adiciona a nova jogadora à lista.
        # Abre o arquivo em modo de escrita ('w') e salva o banco de dados atualizado.
        with open(database_path, "w") as pl:
            dump(db, pl)

# Classe que representa o modelo de dados de um Time.
class Teams():
    # Método construtor para criar uma nova instância de Teams.
    def __init__(self, team_name, president_name, email, phone, state, cnpj = None, players = ""):
        self.id = uuid7str()
        self.cnpj = cnpj if cnpj != None else "NAO INFORMADO"
        self.team_name = team_name
        self.president_name = president_name
        self.email = email
        self.phone = phone
        self.state = state
        self.players = players

    # Métodos comentados que poderiam ser usados para validações futuras.
    # @property
    # def players(self):
    #     return self.players

    # @property.setter
    # def players(self, value):
    #     # Verificar se o CPF de cada jogadora é válido
    #     pass

    # Método estático para ler e retornar apenas a lista de times do banco de dados.
    @staticmethod
    def readTeams():
        with open(database_path, 'r') as tm:
            data = load(tm)
        return data['teams']
    
    # Método para escrever a instância atual do time no banco de dados.
    def writeTeams(self):
        db = readDatabase()

        newTeam = self.__dict__
        
        # Se houver jogadoras na lista, converte cada objeto Player para um dicionário.
        if newTeam['players']:
            for i in range(len(newTeam["players"])):
                newTeam['players'][i] = newTeam['players'][i].__dict__

        db['teams'].append(newTeam) # Adiciona o novo time à lista.
        # Salva o banco de dados atualizado.
        with open(database_path, 'w') as tm:
            dump(db, tm)

    # Método estático auxiliar para formatar dados de jogadoras (atualmente não utilizado de forma completa).
    @staticmethod
    def formatPlayers(newPlayer):
        formatedPlayers = list()
        formatedPlayers.append({"id": newPlayer.id, "cpf": newPlayer.cpf, "name": newPlayer.name})
        return formatedPlayers


# Classe placeholder para futuros desenvolvimentos de Eventos.
class Events():
    pass