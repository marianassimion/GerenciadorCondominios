# 🏢 Sistema de Gerenciamento de Condomínios

Este projeto tem como objetivo desenvolver um **Sistema de Gerenciamento de Condomínios** capaz de modernizar e otimizar os processos administrativos realizados por gestores condominiais. A solução foi projetada para oferecer maior controle, organização e acessibilidade às informações essenciais do condomínio.

---

## 📌 Sobre o Projeto

Este sistema está sendo desenvolvido no contexto da disciplina de **Banco de Dados** do semestre **2025.2** da **Universidade de Brasília (UnB)**.


## 🚀 Tecnologias Utilizadas

- Python 3.12
- Streamlit
- MySQL
- MySQL Connector Python
- Git & GitHub

---

## 📁 Estrutura do Projeto

```
GerenciadorCondominios/
├── main.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── docs/
│   ├── relatorio.pdf
│   └── manual_usuario.pdf
│
├── media/
│   ├── MER.jpg
│   └── MR.jpg
│
├── pages/
│   ├── home.py
│   ├── listagemMoradores.py
│   ├── edicaoMorador.py
│   ├── listagemMoradorResidencia.py
│   ├── listagemResidencias.py
│   └── ...
│
├── src/
│   ├── db_functions.py
│   └── interface/
│       └── img/
│           ├── apt.png
│           ├── morador.png
│           └── ...
│
└── database/
    ├── script_relacionamentos.sql
    ├── script_inserts.sql
    ├── script_procedure.sql
    ├── script_trigger.sql
    └── script_view.sql
```
---

# 🗒️ DESCRIÇÃO DE CADA PASTA DO PROJETO 

## 📁 Organização das Pastas do Projeto

A estrutura do projeto está organizada da seguinte forma:

### 🔹 `main.py`
Arquivo principal do projeto. É o ponto de entrada do sistema e responsável por iniciar a aplicação Streamlit.

---

### 🔹 `config.py`
Arquivo de configuração da conexão com o banco de dados MySQL. Contém as credenciais do banco utilizadas pelo sistema.

---

### 🔹 `requirements.txt`
Arquivo que lista todas as dependências do projeto, permitindo que qualquer pessoa instale rapidamente tudo que é necessário para executar o sistema.

---

### 🔹 `docs/`
Contém toda a documentação do projeto:
- `relatorio.pdf`: relatório do projeto

---

### 🔹 `media/`
Armazena os diagramas do banco de dados:
- `MER.jpg`: Modelo Entidade-Relacionamento
- `MR.jpg`: Modelo Relacional
- `Camada_de_Persistencia.png`: Acesso da interface ao banco de dados
---

### 🔹 `pages/`
Contém todas as telas do sistema desenvolvidas com Streamlit. Cada arquivo representa uma funcionalidade da aplicação, como:
- Tela de condomínios
- Login
- Gerenciamento de moradores
- Veículos
- Taxas
- Entre outras funcionalidades

---

### 🔹 `src/`
Pasta que contém a camada de persistência
- `db_functions.py`: Camada de persistência responsável por todas as operações no banco de dados (INSERT, SELECT, UPDATE, DELETE).
- `interface/img/`: Contém as imagens utilizadas na interface do sistema.

---

### 🔹 `database/`
Pasta que contém todos os scripts SQL utilizados no projeto:
- `script_relacionamentos.sql`: 
- `script_inserts.sql`: inserção de dados iniciais (5 por tabela)
- `script_procedure`: criação da procedure
- `script_trigger.sql`: criação do trigger
- `script_view.sql`: criação da view
---

## 🚀 Como Rodar o Projeto

Siga este passo a passo para configurar o ambiente e executar o sistema na sua máquina.

### 1️⃣ Pré-requisitos
Antes de começar, certifique-se de ter instalado:
* [Python 3.12+](https://www.python.org/downloads/)
* [MySQL Server](https://dev.mysql.com/downloads/mysql/) 
---

### 2️⃣ Configuração do Banco de Dados

1. Abra o MySQL e crie um novo banco de dados vazio com o nome `condominio`.
2. Execute os scripts SQL localizados na pasta `database/` **exatamente nesta ordem**:
   1. `script_relacionamentos.sql` 
   2. `script_inserts.sql` 
   3. `script_view.sql` 
   4. `script_procedure.sql` 
   5. `script_trigger.sql` 

---

### 3️⃣ ⚠️ Configuração da Conexão 

Para que o sistema se conecte ao seu banco de dados local, você **precisa** editar o arquivo de configuração.

1. Na raiz do projeto, localize e abra o arquivo **`config.py`**.
2. Altere os valores das variáveis para corresponderem ao seu MySQL local.

Exemplo de como o arquivo deve ficar:

```python
# config.py

db_config = {
    'host': 'localhost',          # Geralmente é 'localhost'
    'user': 'root',               # Seu usuário do MySQL (ex: root)
    'password': 'SUA_SENHA_AQUI', # <--- COLOQUE A SENHA DO SEU BANCO AQUI
    'database': 'condominio_db'   # O nome do banco que você criou no passo anterior
}
```

## 4️⃣ Instalação das Dependências
Abra o terminal na pasta raiz do projeto (GerenciadorCondominios/) e execute:
```python
    python -m venv venv

    #Windows:
    venv\Scripts\activate

    #Linux/Mac:
    source venv/bin/activate

    # Instale as bibliotecas necessárias
    pip install -r requirements.txt
}
```
## 5️⃣ Executando o Sistema
Com tudo configurado, execute o comando abaixo para iniciar a interface:

```Bash

streamlit run main.py
```
