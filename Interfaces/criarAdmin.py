## Arquivo temporário
import mysql.connector
import bcrypt
from pages.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME 

conexao = mysql.connector.connect(
    host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
)
cursor = conexao.cursor()

email = "mariana@condo.com"
nome = "Mariana"
senha_texto = "123" 

# Gera o Hash
salt = bcrypt.gensalt()
senha_hash = bcrypt.hashpw(senha_texto.encode('utf-8'), salt)

try:
    cursor.execute(
        "INSERT INTO ADMINISTRADOR (email, nome, senha) VALUES (%s, %s, %s)",
        (email, nome, senha_hash)
    )
    conexao.commit()
    print("✅ Administrador criado com sucesso!")
    print(f"Login: {email}")
    print(f"Senha: {senha_texto}")
except Exception as e:
    print(f"Erro: {e}")
finally:
    cursor.close()
    conexao.close()
