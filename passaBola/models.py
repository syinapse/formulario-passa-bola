from requests import post
from json import dump, load, dumps
from uuid_extensions import uuid7str
from wtforms import ValidationError
from passaBola import cpf_api_key
from pathlib import Path
from datetime import datetime
database_path = Path("./passaBola/database/database.json")

def readDatabase():
    with open(database_path, "r") as db:
        data = load(db)
    return data


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

    data = post(url, json=data, headers=header).json()
    return data


class Player():
    def __init__(self, cpf, full_name, birthday, email, phone, state, instagram = None):
        self.id = uuid7str() # Id único aleatório em UUID7
        self.cpf = cpf
        self.full_name = full_name
        self.birthday = birthday
        self.email = email
        self.phone = phone
        self.state = state
        self.instagram = instagram if instagram != None else "INEXISTENTE"

    @classmethod
    def TeamsPlayers(cls, cpf, name):
        return cls(cpf=cpf, full_name=name, birthday=None, email=None, phone=None, state=None)

    @staticmethod
    def readPlayers():
        with open(database_path, "r") as pl:
            data = load(pl)
        return data["players"]
    
    def witeNewPlayer(self):
        db = readDatabase() # Todo o banco de dados
        newPlayer = self.__dict__ # Converte o objeto Player para um dicionário
        newPlayer['birthday'] = newPlayer['birthday'].strftime("%d-%m-%Y")
        db['players'].append(newPlayer)
        with open(database_path, "w") as pl:
            dump(db, pl)

class Teams():
    def __init__(self, cnpj, team_name, president_name, email, phone, state, players = ""):
        self.id = uuid7str()
        self.cnpj = cnpj
        self.team_name = team_name
        self.president_name = president_name
        self.email = email
        self.phone = phone
        self.state = state
        self.players = players


    # @property
    # def players(self):
    #     return self.players

    # @property.setter
    # def players(self, value):
    #     # Verificar se o CPF de cada jogadora é válido
    #     pass

    @staticmethod
    def readTeams():
        with open(database_path, 'r') as tm:
            data = load(tm)
        return data['teams']
    
    def writeTeams(self):
        db = readDatabase()

        newTeam = self.__dict__
        
        if newTeam['players']:
            for i in range(len(newTeam["players"])):
                newTeam['players'][i] = newTeam['players'][i].__dict__

        db['teams'].append(newTeam)
        with open(database_path, 'w') as tm:
            dump(db, tm)

    @staticmethod
    def formatPlayers(newPlayer):
        formatedPlayers = list()
        formatedPlayers.append({"id": newPlayer.id, "cpf": newPlayer.cpf, "name": newPlayer.name})
        
        print(f'Formated Players: {formatedPlayers}')
        return formatedPlayers



class Events():
    pass