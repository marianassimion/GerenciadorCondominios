import mysql.connector
conexao = mysql.connector.connect(
    host ='localhost',
    user ='Mariana',
    password='Mariana.89',
    database= 'condominio'
)

cursor = conexao.cursor()

#CRUD

#CREATE
cnpj = '1234567012'
nome = 'TesteNomeCondominio Python 1'
endereco = 'TesteEndereco Python 1'

comando = f'INSERT INTO condominio (cnpj, nome, endereco) VALUES ("{cnpj}", "{nome}", "{endereco}")'
cursor.execute(comando) #executa o comando
conexao.commit()#salva as alterações, caso o comando seja de edição
resultado = cursor.fetchall()#ler o banco de dados


#READ
#comando = f'SELECT * FROM vendas'
#cursor.execute(comando)
#resultado = cursor.fetchall()#ler o banco de dados
#print(resultado)

#UPDATE
#nome_produto = ""
#valor = 6
#comando = f'UPDATE vendas SET  valor = {valor}  WHERE nome_produto = "{nome_produto}"'

cursor.close()
conexao.close()
