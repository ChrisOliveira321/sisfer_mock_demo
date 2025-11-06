SISFER Mock Demo

Projeto de demonstração do SISFER, criado para simular o envio e gerenciamento de carregamentos de forma automática, incluindo um front-end simples e integração via Excel. Ideal para testes e aprendizado sobre APIs, autenticação e CRUD.


---

Funcionalidades

Simula login de usuário com geração de token.

Permite criar, listar e consultar carregamentos.

Front-end básico em HTML/JS para interagir com a API.

Uploader de Excel: envia várias cargas de uma planilha de uma vez.

Banco de dados SQLite integrado para persistência dos dados.



---

Tecnologias

Python 3

Flask

Flask-SQLAlchemy

Flask-CORS

SQLite

JavaScript (Front-end)

Pandas (para ler Excel)



---

Instalação

1. Clone o repositório:



git clone https://github.com/ChrisOliveira321/sisfer_mock_demo.git
cd sisfer_mock_demo

2. Crie e ative um virtualenv:



python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

3. Instale as dependências:



pip install -r requirements.txt

4. Rodar a API mock:



python mock_sisfer_api.py

O servidor vai rodar em http://127.0.0.1:5000.

5. Abrir o front-end:



Abra o arquivo index.html no navegador.


6. Rodar o uploader de Excel:



python excel_uploader.py

> A planilha deve ter as colunas: Placa, Produto, Peso.




---

Usuário de Teste

Usuário: transp1

Senha: senha123



---

Endpoints da API

POST /login → autenticação e geração de token.

GET /status → status da API.

POST /carregamentos → cria um carregamento (autenticado).

GET /carregamentos → lista carregamentos do usuário.

GET /carregamentos/<id> → detalhes de um carregamento.

DELETE /carregamentos/<id> → deletar carregamento (atualmente apenas via código).



---

Como Funciona

1. O front-end envia os dados para a API mock.


2. A API valida o token e armazena os carregamentos no SQLite.


3. O uploader de Excel permite enviar várias linhas de uma planilha automaticamente.


4. Ideal para testar integrações sem mexer em sistemas reais.




---

Observações

Projeto apenas para demo e aprendizado.
Não deve ser usado em produção (ainda hahaha)

O back-end e o front-end estão integrados localmente.

---
