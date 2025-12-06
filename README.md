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

```bash
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
    └── view.sql
