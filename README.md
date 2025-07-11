# Cogito

Este é o Cogito, uma plataforma de cursos voltada para educadores e professores brasileiros. Este repositório contém a
API RESTful do projeto, o back-end. O framework escolhido foi o Python FastAPI, junto do ORM Peewee, com MySQL como
SGBD.

## Instruções de execução local

> É preciso ter o `Python 3.10` ou mais recente, MySQL 8.0 ou mais recente, além do `git`.

Antes de configurar a aplicação Python, crie o usuário `cogito_dba` com a senha `1234`, concedendo acesso a ele aos
bancos de dados criados.

1. Clone este repositório. `git clone https://gitlab.com/isaque-dantas/cogito-server.git`
2. Mude o diretório atual para a pasta clonada. `cd cogito-server`
3. Crie um ambiente virtual do Python. `python3 -m venv .venv` (Linux / macOS) ou `python -m venv .venv` (Windows)
4. Ative o ambiente virtual do Python. `source .venv/bin/activate` (Linux / macOS) ou
   `.\.venv\Scripts\activate` (Windows)
5. Instale as dependências. `pip install -r requirements.txt`
6. Crie os esquemas do banco de dados. Inicie um console interativo: `python`, importe a função de inicialização do banco de dados:
   `from app.models import create_db_and_tables` e execute-a: `create_db_and_tables()`
7. Execute a aplicação. `fastapi run app`
