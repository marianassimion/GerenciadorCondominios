import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME # Importa do config.py
from flask import Flask, make_response, jsonify, request
#from flask_cors import CORS # Importe o CORS


app = Flask('Gerenciador') #instanciando o flask na variável app
app.config['JSON_SORT_KEYS'] = False
#CORS(app)

def get_db_connection():
    try:
        conexao = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conexao.cursor(dictionary=True)
        print('Conexão bem-sucedida')
        return conexao, cursor
    except mysql.connector.Error as err:
        print(f"Erro ao conectar no MySQL: {err}")
        #exit()
        return None, None



@app.route('/condominios', methods=['GET'])

def get_condominios():
    conexao, cursor = get_db_connection()

    if conexao is None:
        return jsonify(erro="Não foi possível ligar a base de dados"), 500

    try:
        cursor.execute('SELECT * FROM condominio')
        meus_condominios = cursor.fetchall()
        print(meus_condominios)
        return make_response(
            jsonify(
                mensagem = 'Lista de condomínios',
                dados = meus_condominios
            )
        )
    
    except mysql.connector.Error as err:
        return jsonify(erro=f"Erro ao consultar: {err}"), 400
    
    finally:
        # 3. Fechar a conexão e o cursor DEPOIS de os usar
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()
            

if __name__ == '__main__':
    print("Iniciando o servidor Flask em http://127.0.0.1:5000/")
    app.run(debug=True)