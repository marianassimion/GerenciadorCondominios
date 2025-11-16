import mysql.connector
#import time
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME # Importa do config.py
from flask import Flask

app = Flask('Gerenciador') #instanciando o flask na variável app

@app.route('/Condominios', methods=['GET'])

def get_condominios():
     return Condominios

app.run()

try:
    conexao = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conexao.cursor()
    print('Conexão bem-sucedida')

except mysql.connector.Error as err:
    print(f"Erro ao conectar no MySQL: {err}")
    exit()


def criar_condominio(cnpj, nome, endereco):
    comando = f'INSERT INTO condominio (cnpj, nome, endereco) VALUES (%s, %s, %s)'
    valores = (cnpj, nome, endereco)

    try:
        cursor.execute(comando, valores) # Executa o comando seguro
        conexao.commit()                 # Salva as alterações
        print(f"Condomínio '{nome}' criado com sucesso!")

    except mysql.connector.Error as err:
        print(f"Erro ao inserir condomínio: {err}")
        conexao.rollback() # Desfaz a operação em caso de erro

def criar_administrador(email, nome, senha):
    comando = f'INSERT INTO ADMINISTRADOR(email, nome, senha) VALUES (%s, %s, %s)'
    valores = (email, nome, senha)
    try:
        cursor.execute(comando, valores)
        conexao.commit()
        print(f"Administrador '{nome}' criado com sucesso!")
    
    except mysql.connector.Error as err:
        print(f"Erro ao inserir administrador: {err}")
        conexao.rollback()

def listar_condominios():
    comando = "SELECT cnpj FROM CONDOMINIO"
    try:
        cursor.execute(comando)
        resultados = cursor.fetchall()
        return resultados
    except mysql.connector.Error as err:
        print(f"Erro ao consultar condomínios: {err}")
        return []

def criar_residencia(condominio_cnpj, num_unidade, bloco, endereco):
    comando = f'INSERT INTO RESIDENCIA(condominio_cnpj, num_unidade, bloco, endereco) VALUES (%s, %s, %s, %s)'
    valores = (condominio_cnpj, num_unidade, bloco, endereco)
    try:
        cursor.execute(comando, valores)
        conexao.commit()
        print(f"Residência de número '{num_unidade}' criada com sucesso!")
        
    except mysql.connector.Error as err:
        print(f"Erro ao criar residencia: {err}")
        conexao.rollback()

def criar_empregado(cpf, nome, cargo, matricula, data_admissao, salario, condominio_cnpj):
    comando = f'INSERT INTO EMPREGADO(cpf, nome, cargo, matricula, data_admissao, salario, condominio_cnpj) VALUES (%s, %s, %s, %s, %s, %s, %s)'                                              
    valores = (cpf, nome, cargo, matricula, data_admissao, salario, condominio_cnpj)
    try:
        cursor.execute(comando, valores)
        conexao.commit()
        print(f"Empregado '{nome}' cadastrado com sucesso!")
    
    except mysql.connector.Error as err:
        print(f"Erro ao inserir empregado: {err}")
        conexao.rollback()

def criar_aviso(titulo, texto, id_administrador):
    comando = f'INSERT INTO AVISO(titulo, texto, id_administrador) VALUES (%s, %s, %s)'
    valores = (titulo, texto, id_administrador)
    try:
        cursor.execute(comando, valores)
        conexao.commit()
        print(f"Aviso '{titulo}' criado com sucesso!")
        
    except mysql.connector.Error as err:
        print(f"Erro ao criar aviso: {err}")
        conexao.rollback()

def criar_morador(cpf, nome, email, id_residencia):
        comando = f'INSERT INTO MORADOR(cpf, nome, email, id_residencia) VALUES (%s, %s, %s, %s)'
        valores = (cpf, nome, email, id_residencia)
        try:
            cursor.execute(comando, valores)
            conexao.commit()
            print(f"Morador '{nome}' criado com sucesso!")
            
        except mysql.connector.Error as err:
            print(f"Erro ao criar morador: {err}")
            conexao.rollback()

def criar_visitante(rg, nome, id_residencia):
        comando = f'INSERT INTO VISITANTE(rg, nome, id_residencia) VALUES (%s, %s, %s)'
        valores = (rg, nome, id_residencia)
        try:
            cursor.execute(comando, valores)
            conexao.commit()
            print(f"Visitante '{nome}' para a residência {id_residencia} criado com sucesso!")
            
        except mysql.connector.Error as err:
            print(f"Erro ao criar visitante: {err}")
            conexao.rollback()

def criar_multa(status_pagamento, valor, descricao, id_residencia):
        comando = f'INSERT INTO MULTA(status_pagamento, valor, descricao, id_residencia) VALUES (%s, %s, %s, %s)'
        valores = (status_pagamento, valor, descricao, id_residencia)
        try:
            cursor.execute(comando, valores)
            conexao.commit()
            print(f"Multa '{descricao}' no valor de R${valor} para a residência {id_residencia} criada com sucesso!")            
        except mysql.connector.Error as err:
            print(f"Erro ao criar multa: {err}")
            conexao.rollback()

def criar_taxa(status_pagamento, valor, descricao, id_residencia):
        comando = f'INSERT INTO TAXA(status_pagamento, valor, descricao, id_residencia) VALUES (%s, %s, %s, %s)'
        valores = (status_pagamento, valor, descricao, id_residencia)
        try:
            cursor.execute(comando, valores)
            conexao.commit()
            print(f"Taxa '{descricao}' no valor de R${valor} para a residência {id_residencia} criada com sucesso!")            
        except mysql.connector.Error as err:
            print(f"Erro ao criar taxa: {err}")
            conexao.rollback()

def criar_veiculo(placa, modelo, cor, morador_cpf):
        comando = f'INSERT INTO VEICULO(placa, modelo, cor, morador_cpf) VALUES (%s, %s, %s, %s)'
        valores = (placa, modelo, cor, morador_cpf)
        try:
            cursor.execute(comando, valores)
            conexao.commit()
            print(f"Veículo '{modelo}' de placa '{placa}' vinculado ao morador {morador_cpf} criado com sucesso!")
            
        except mysql.connector.Error as err:
            print(f"Erro ao criar veículo: {err}")
            conexao.rollback()




cursor.close()
conexao.close()
print("Conexão fechada")
