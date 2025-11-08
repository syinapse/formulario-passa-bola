# ⚽ Formulário de Eventos Passa a Bola

Aplicação web de cadastro de jogadoras e equipes para a competição **Copa Passa a Bola**, desenvolvida em **Python (Flask)**, **JavaScript** e **LocalStorage**.  
Todas as inscrições (jogadoras e times) são armazenadas em uma base de dados local em formato **JSON**, com senhas criptografadas.

---

## Desenvolvido por Synapse
* Carlos Eduardo Sanches Mariano RM: 561756
* Leonardo Eiji Kina RM: 562784
* Luís Scacchetti Mariano RM: 562241
* Rodrigo do Santos Abubakir RM: 561479
* Vitor Ramos de Farias RM: 561958


## 📋 Sumário
- [Características Principais](#características-principais)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Como Executar](#como-executar)
- [Banco de Dados e Exemplo](#banco-de-dados-e-exemplo)
- [APIs Externas](#apis-externas)
- [Contribuição](#contribuição)

---

## 🏆 Características Principais
- Cadastro de **jogadoras** individuais e **times** para o evento.
- Cada jogadora e cada time possuem um **UUID único**.
- Validação de documentos **CPF/CNPJ** via API externa.
- Consulta e validação de **UFs e endereços**.
- Armazenamento em **arquivos JSON** para prototipagem local.
- Interface simples e responsiva para gestão dos cadastros.
- Integração com **Flask** para rotas dinâmicas.
- Painel administrativo para criação e listagem de eventos.

---

## 🧠 Tecnologias Utilizadas
- **Python 3.x**
- **Flask**
- **HTML5 / CSS3 / JavaScript**
- **Bootstrap 5**
- **APIs**: BrasilAPI
- **Armazenamento local**: JSON

---

## 📂 Estrutura do Projeto

```
formulario-passa-bola/
│
├── passaBola/                 # Código principal da aplicação Flask
│   ├── static/                # Arquivos estáticos (CSS, JS, imagens)
│   ├── templates/             # Templates HTML com Jinja2
│   ├── models/                # Classes e lógica de banco de dados
│   └── __init__.py
│
├── run.py                     # Script para inicializar o servidor Flask
├── requirements.txt           # Dependências do projeto
└── database/                  # Armazenamento em JSON (usuários e eventos)
```

---

## 🚀 Como Executar

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/syinapse/formulario-passa-bola.git
   cd formulario-passa-bola
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate    # Windows
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o servidor Flask:**
   ```bash
   python run.py
   ```

5. Acesse no navegador:
   ```
   http://localhost:5000
   ```

---

## 🗃️ Banco de Dados e Exemplo

Os dados são armazenados em formato JSON no diretório `database/`.  
Exemplo de estrutura de usuário:

```json
{
  "019a42d2-46ca-782c-9956-ef6c5f56ea52": {
    "username": "teste",
    "email": "teste@gmail.com",
    "password": "hash",
    "cpf": "12345678901",
    "phone": "11987654321",
    "state": "SP",
    "events": ["0690ab9a-eeaa-7266-8000-0e64d947c292"]
  }
}
```

---

## 🌎 APIs Externas

O sistema utiliza as seguintes APIs para validações e preenchimento automático:

- [BrasilAPI](https://brasilapi.com.br) — validação de CEP e estados.  

---

## 🤝 Contribuição

Contribuições são bem-vindas!  
1. Faça um fork do projeto.
2. Crie uma branch com sua feature (`git checkout -b minha-feature`).  
3. Faça o commit (`git commit -m 'feat: adiciona nova funcionalidade'`).  
4. Envie o push (`git push origin minha-feature`).  
5. Abra um Pull Request!

---
