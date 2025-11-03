from json import dump, load
from uuid_extensions import uuid7str
from pathlib import Path
from flask_login import UserMixin
from passaBola import bcrypt, loginManager

database_path = Path("./passaBola/database/database.json")

def readDatabase():
    with open(database_path, "r") as db:
        data = load(db)
    return data

@loginManager.user_loader
def load_user(user_id):
    return User.findUserById(user_id)

# # Função para validar um CPF e data de nascimento através de uma API externa.
# def checkCPF(cpf, birthday):
#     url = "https://api.cpfhub.io/api/cpf"
#     header = {
#         "x-api-key": cpf_api_key,
#         "Content-Type": "application/json"

#     }
#     data = {
#         "cpf": cpf,
#         "birthDate": birthday
#     }

#     # Envia a requisição POST para a API e retorna a resposta em formato JSON.
#     data = post(url, json=data, headers=header).json()
#     return data

class Player():
    def __init__(self, cpf, full_name, birthday, email, phone, state, instagram = None):
        self.id = uuid7str() # 
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
        db = readDatabase()
        newPlayer = self.__dict__ 
        newPlayer['birthday'] = newPlayer['birthday'].strftime("%d-%m-%Y")
        db['players'].append(newPlayer)
        with open(database_path, "w") as pl:
            dump(db, pl)

class Teams():
    def __init__(self, team_name, president_name, email, phone, state, cnpj = None, players = ""):
        self.id = uuid7str()
        self.cnpj = cnpj if cnpj != None else "NAO INFORMADO"
        self.team_name = team_name
        self.president_name = president_name
        self.email = email
        self.phone = phone
        self.state = state
        self.players = players

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
        return formatedPlayers


# Classe placeholder para futuros desenvolvimentos de Eventos.
class Events():
    def __init__(self, title, address, state, begin_date, end_date, event_description, reward_description, min_age, max_age, max_uni_sub, max_team_sub, cost_uni_sub = 0, cost_team_sub = 0, linkedin = "", instagram = "", whats = "", other = ""):
        self.title = title
        self.address = address
        self.state = state
        self.eventDates = {"start": begin_date, "end": end_date}
        self.event_description = event_description
        self.reward_description = reward_description
        self.eventAge = {"min": min_age, "max": max_age}
        self.totalPlayers = max_uni_sub
        self.totalTeams = max_team_sub
        self.eventCostPlayer = cost_uni_sub
        self.eventCostTeam = cost_team_sub
        self.linkedin = linkedin
        self.instagram = instagram
        self.whatsapp = whats
        self.other = other


class User(UserMixin):
    def __init__(self, username, email, cpf, phone, state, password='senhaTemp'):
        self.id = uuid7str()
        self.cpf = cpf
        self.username = username
        self.password = password
        self.hashPassword = None
        self.email = email
        self.phone = phone
        self.state = state

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, value):
        self.hashPassword = bcrypt.generate_password_hash(value).decode('utf-8')

    def isValidPassword(self, attempedPassword):
        return bcrypt.check_password_hash(self.hashPassword, attempedPassword)
    
    @classmethod
    def findUserByEmail(cls, email):
        all_users = User.readUsers()
        for user_data in all_users:
            if user_data['email'] == email:
                user = cls(username=user_data['username'],
                                email=user_data['email'],
                                cpf=user_data['cpf'],
                                phone=user_data['phone'],
                                state=user_data['state'])
                user.id = user_data['id'] # Garante que o ID seja o mesmo do banco
                user.hashPassword = user_data['password'];
                return user
        return None
    
    @classmethod
    def findUserById(self, userid):
        all_users = User.readUsers()
        for user_data in all_users:
            # user_id vem como string, o id no seu JSON é um número
            if user_data['id'] == userid:
                # Recria o objeto User com os dados do "banco"
                # Importante: Não passe a senha aqui para não hashear de novo!
                user = User(username=user_data['username'],
                                email=user_data['email'],
                                password=user_data['password'],
                                cpf=user_data['cpf'],
                                phone=user_data['phone'],
                                state=user_data['state'])
                user.id = user_data['id'] # Garante que o ID seja o mesmo do banco
                return user
        return None
    
    @staticmethod
    def readUsers():
        """
        Read all users registered in the system
        """
        with open(database_path, "r") as f:
            data = load(f)
        return data['users']

    @classmethod
    def writeNewUser(self):
        """
        Write the current new user created on JSON database
        """
        data = readDatabase()
        newUser = { "id": self.id,
                    "username": self.username,
                    "email": self.email,
                    "password": self.hashPassword,
                    "cpf": self.cpf,
                    "phone": self.phone,
                    "state": self.state  
                    }
        data['users'].append(newUser)
        with open(database_path, "w") as f:
            dump(data, f)


# class Database():
#     @staticmethod
#     def readUsers(key):
#         """
#         Read all users registered in the system
#         """
#         with open(database_path, "r") as f:
#             data = load(f)
#         return data[key]

#     @staticmethod
#     def writeNewUser(self):
#         """
#         Write the current new user created on JSON database
#         """
#         data = readDatabase()
#         newUser = { "id": self.id,
#                     "username": self.username,
#                     "email": self.email,
#                     "password": self.hashPassword,
#                     "cpf": self.cpf,
#                     "phone": self.phone,
#                     "state": self.state  
#                     }
#         data['users'].append(newUser)
#         with open(database_path, "w") as f:
#             dump(data, f)