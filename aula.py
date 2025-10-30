import mysql.connector
#import bcrypt

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


criar_condominio('55555555', 'teste função', 'teste endereço função')

criar_administrador("teste@adm5",'Adm5',"teste 5")


cursor.close()
conexao.close()
print("Conexão fechada")
