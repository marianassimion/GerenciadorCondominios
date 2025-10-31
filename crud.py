import mysql.connector
#import bcrypt
import time
try:
    conexao = mysql.connector.connect(
        host ='localhost',
        user ='Mariana',
        password='Banco.123',
        database= 'condominio'
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


criar_aviso('aviso 1', 'tentando criar um aviso sem usar o timestamp no código em python', 2)

#condominios = listar_condominios()
#print (*condominios)


#criar_residencia('45645464','002', 'B', 'Teste 2 de criar residencia' )
#criar_residencia('1234567891012','003', 'C', 'Teste 3 de criar residencia' )

cursor.close()
conexao.close()
print("Conexão fechada")
