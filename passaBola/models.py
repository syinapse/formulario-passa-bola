from json import dump, load
from uuid_extensions import uuid7str
from pathlib import Path
from flask_login import UserMixin
from passaBola import bcrypt, loginManager

database_path = Path("./passaBola/database/database.json")

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
    
    def writeNewPlayer(self, event_id):
        db = Database.readDatabase(Database.db_registers)
        newPlayer = self.__dict__ 
        newPlayer['birthday'] = newPlayer['birthday'].strftime("%d-%m-%Y")
        if event_id not in db.keys():
            db[event_id] = {
                "players": [],
                "teams": []
            }
        db[event_id]['players'].append(newPlayer)
        with open(Database.db_registers, "w") as pl:
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
    
    def writeTeams(self, event_id):
        db = Database.readDatabase(Database.db_registers)

        newTeam = self.__dict__.copy()
        newTeam["players"] = [p.__dict__.copy() for p in self.players] if self.players else []

        if event_id not in db:
            db[event_id] = {"players": [], "teams": []}

        db[event_id]["teams"].append(newTeam)

        with open(Database.db_registers, "w") as tm:
            dump(db, tm)


    @staticmethod
    def formatPlayers(newPlayer):
        formatedPlayers = list()
        formatedPlayers.append({"id": newPlayer.id, "cpf": newPlayer.cpf, "name": newPlayer.name})
        return formatedPlayers


# Classe placeholder para futuros desenvolvimentos de Eventos.
class Events():
    def __init__(self, title, address, state, begin_date, end_date, event_description, reward_description, min_age, max_age, max_uni_sub, max_team_sub, cost_uni_sub = 0, cost_team_sub = 0, linkedin = "", instagram = "", whats = "", other = ""):
        
        def getDates():
            start = begin_date
            end = end_date
            if type(begin_date) != str:
                start = begin_date.strftime("%d-%m-%Y")
            
            if type(end_date) != str:
                end = end_date.strftime("%d-%m-%Y")
            return {"start": start, "end": end}
        
        self.id = uuid7str()
        self.title = title
        self.address = address
        self.state = state
        self.eventDates = getDates()
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

    @classmethod
    def findEventById(cls, event_id):
        try:
            all_events: dict = Database.readDatabase(Database.db_events)
            if (event_id not in all_events.keys()):
                return None
            foundedEvent = all_events[event_id]
            event = cls(
                title=foundedEvent['title'],
                address=foundedEvent['address'],
                state=foundedEvent['state'],
                begin_date=foundedEvent['eventDates']['start'],
                end_date=foundedEvent['eventDates']['end'],
                event_description=foundedEvent['event_description'],
                reward_description=foundedEvent['reward_description'],
                min_age=foundedEvent['eventAge']['min'],
                max_age=foundedEvent['eventAge']['max'],
                max_uni_sub=foundedEvent['totalPlayers'],
                max_team_sub=foundedEvent['totalTeams'],
                cost_team_sub=foundedEvent['eventCostTeam'],
                cost_uni_sub=foundedEvent['eventCostPlayer'],
                linkedin=foundedEvent['linkedin'],
                instagram=foundedEvent['instagram'],
                whats=foundedEvent['whatsapp'],
                other=foundedEvent['other']
            )
            event.id = event_id
            return event
        except Exception:
            raise

        return None
    
    def writeNewEvent(self, user_id):
        """
        Write the current new user created on JSON database
        """
        path = Database.db_events
        data:dict = Database.readDatabase(path)
        users:dics = Database.readDatabase(Database.db_profile)
        newEvent = self.__dict__.copy()
        del newEvent['id']
        data[self.id] = (newEvent)
        users[user_id]['events'].append(self.id)
        with open(path, "w") as f:
            dump(data, f)
        with open(Database.db_profile, "w") as f:
            dump(users, f)


class User(UserMixin):
    def __init__(self, username, email, cpf, phone, state, events = [], password:str = 'senhaTemp'):
        self.id = uuid7str()
        self.cpf = cpf
        self.username = username
        self.password = password
        self.hashPassword = None
        self.email = email
        self.phone = phone
        self.state = state
        self.events = events

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
        try:
            all_users: dict = Database.readDatabase(Database.db_profile)
            for uuid, data in all_users.items():
                if data['email'] == email:
                    return cls.findUserById(uuid)
            return None
        except Exception:
            raise
    
    @classmethod
    def findUserById(cls, userid):
        try:
            all_users: dict = Database.readDatabase(Database.db_profile)
            if (userid not in all_users.keys()):
                return None
            foundedUser = all_users[userid]
            user = cls(
                foundedUser['username'],
                foundedUser['email'],
                foundedUser['cpf'],
                foundedUser['phone'],
                foundedUser['state'],
                foundedUser['events'])
            user.id = userid
            user.hashPassword = foundedUser['password'];
            return user
        except Exception:
            raise

        return None
    
    def writeNewUser(self):
        """
        Write the current new user created on JSON database
        """
        path = Database.db_profile
        data = Database.readDatabase(path)
        newUser = self.__dict__.copy()
        del newUser['id']

        data[self.id].append(newUser)
        with open(path, "w") as f:
            dump(data, f)


class Database():
    db_profile = Path("./passaBola/database/profiles.json")
    db_events = Path("./passaBola/database/events.json")
    db_registers = Path("./passaBola/database/events_registers.json")
    db_main = Path("./passaBola/database/database.json")

    @staticmethod
    def readDatabase(database_path = db_main):
        with open(database_path, "r") as db:
            data: dict = load(db)
        return data

    @staticmethod
    def readData(database_path, key:str):
        """
        Read all data registered in the system from a key
        """
        try:
            if not Path(database_path).exists():
                with open(database_path, "w") as db:
                    dump(dict(), db)
                return dict()

            with open(database_path, "r") as f:
                data = load(f)
            return data[key]
        except KeyError:
            raise KeyError("A chave informada é inválida.")
