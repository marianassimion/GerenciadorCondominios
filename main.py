import mysql.connector
import time
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME # Importa do config.py

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

#criar_empregado('123456', 'Empregado 1', 'teste 1', '11111', '2020-11-10', 1000.02, '3333')


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

#criar_residencia('1234567891012', '8', 'B','Testes')

criar_morador('123456', 'teste 1', 'teste1@gmail.com', '7')

cursor.close()
conexao.close()
print("Conexão fechada")
