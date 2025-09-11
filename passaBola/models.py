from requests import post
from json import dump, load, dumps
from uuid_extensions import uuid7str
from passaBola import cpf_api_key
from pathlib import Path
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
    def __init__(self, cpf, full_name, birthday, email, phone, city = "são paulo", instagram = None):
        self.id = uuid7str() # Id único aleatório em UUID7
        self.cpf = cpf
        self.Full_name = full_name
        self.Birthday = birthday
        self.Email = email
        self.Phone = phone
        self.City = city
        self.Instagram = instagram if instagram != None else "Não indicado"

    @staticmethod
    def readPlayers():
        with open(database_path, "r") as pl:
            data = load(pl)
        return data["players"]
    
    def witeNewPlayer(self):
        db = readDatabase() # Todo o banco de dados

        newPlayer = dumps(self.__dict__) # Converte o objeto Player para um dicionário e depois pelo método 'dumps' para um JSON
        print(newPlayer)
        db['players'].append(newPlayer)
        with open(database_path, "w") as pl:
            dump(db, pl)


class Teams():
    def __init__(self, cnpj, team_name, president_name, email, phone, city, players):
        self.id = uuid7str()
        self.Cnpj = cnpj
        self.Team_name = team_name
        self.president_name = president_name
        self.email = email
        self.phone = phone
        self.city = city
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
        newTeam = dumps(self.__dict__)

        db['teams'].append(newTeam)
        with open(database_path, 'w') as tm:
            dump(db, tm)

class Events():
    pass