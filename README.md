# ⚽ Formulário de eventos Passa a bola

O Projeto consiste em um portal web de inscrições de jogadoras e times para o evento **_Copa Passa a bola_** desenvolvido em Python Flask com Javascript, LocalStorage e chamadas de APIs como **BrasilAPI, ReceitaWS e CPFhubIo**. Todas as pessoas e times inscritos são armazenados no _**Database JSON**_ contido no Projeto com seus devidos **documentos criptografados**.

> [!IMPORTANT]
> O Projeto está em desenvolvimento, portanto podem ocorrer bugs
## Desenvolvido por Synapse
* Carlos Eduardo Sanches Mariano RM: 561756
* Leonardo Eiji Kina RM: 562784
* Luís Scacchetti Mariano RM: 562241
* Rodrigo do Santos Abubakir RM: 561479
* Vitor Ramos de Farias RM: 561958


##  Como executar o Projeto

### Clone o Projeto no diretório atual
```bash
git clone https://github.com/syinapse/formulario-passa-bola.git .
```
**_Remova o ponto no final caso deseje criar uma nova pasta para o clone_**
```bash
git clone https://github.com/syinapse/formulario-passa-bola.git

cd formulario-passa-bola/
```

### Instale as dependências
#### Windows, Linux (Debian/Fedora)
```bash
pip install -r requirements.txt
```
#### Distribuições Arch Linux
Crie um ambiente virtual e use o ```pipx```:
```bash
pipx install cookiecutter
pipx runpip cookicutter install -r requirements.txt
```

### Execute o Projeto

#### Windows
```bash
python run.py
```

#### Linux
```bash
python3 run.py
```

## 📂 Estrutura do Database JSON

As inscrições são armazenadas em duas chaves principais:

- **players** → Jogadoras individuais

- **teams** → Times cadastrados

Sempre que um clube adiciona uma jogadora no último campo do formulário, ela também é registrada como jogadora individual no sistema, recebendo um UUIDv7 único.

### 🎯 Exemplo - Jogadoras Individuais
> [!NOTE]
> Os dados abaixo são fictícios e servem apenas para fins ilustrativos.

```json
{
 "players": [
    {
      "id": "068c600c-4b0b-7a57-8000-4e9411cec976",
      "cpf": "1735681531",
      "full_name": "Regina dos Santos",
      "birthday": "02-05-2006",
      "email": "regina@email.com",
      "phone": "11983767352",
      "city": "mg",
      "instagram": "@regina.santos"
    }
 ]
}
```


### 🎯 Exemplo - Times

```json
{
    "teams": [
    {
        "id": "068c633a-4d92-7d38-8000-0bd83740c427",
        "cnpj": "1678361723000151",
        "team_name": "Time de Varzea",
        "president_name": "Pedro Rodigues",
        "email": "pedro@exemplo.com",
        "phone": "11999999999",
        "city": "sp",
        "players": [
            {
                "id": "068c633a-4d92-7eca-8000-b5eb652269b9",
                "cpf": "1234567890",
                "full_name": "Maria de Souza",
                "birthday": null,
                "email": null,
                "phone": null,
                "city": null,
                "instagram": "Nao indicado"
            },
        ]
     }
    ]
}
```


## 🌐 Acesso as APIS utilizadas
- [BrasilAPI](https://brasilapi.com.br/docs#tag/IBGE/paths/~1ibge~1uf~1v1/get): Retorna todos os estados e unidaddes de federação do Brasil
- [ReceitaWS](https://developers.receitaws.com.br/#/operations/queryRFFree): Pesquisa e verifica se o CNPJ informado existe na receita federal.
- [CPFHubio](https://www.cpfhub.io): Pesquisa e verifica se o CPF informado é válido.