# Em app.py (seu novo servidor Flask)

# (Importações no topo do arquivo)
import mysql.connector
from flask import Flask, jsonify
from flask_cors import CORS
# (Não precisamos de 'request' aqui, pois GET não recebe dados no corpo)

app = Flask(__name__)
CORS(app)

# (Função de conexão que criamos antes)
def get_db_connection():
    # ... (código da conexão igual ao da resposta anterior) ...
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='Mariana',
            password='Banco.123',
            database='condominio'
        )
        # Importante: dictionary=True
        # Faz o cursor.fetchall() retornar uma lista de dicionários!
        # Isso economiza o loop de conversão manual.
        return conexao
    except mysql.connector.Error as err:
        print(f"Erro ao conectar: {err}")
        return None

# --- AQUI ESTÁ A MÁGICA DA CONSULTA (GET) ---
@app.route('/api/avisos', methods=['GET'])
def api_listar_avisos():
    
    conexao = get_db_connection()
    if not conexao:
        return jsonify({"erro": "Falha na conexão com o banco"}), 500

    # dictionary=True faz a mágica!
    # Em vez de tuplas (1, 'Aviso 1'), ele retorna dicionários
    # {'id_aviso': 1, 'titulo': 'Aviso 1'}
    cursor = conexao.cursor(dictionary=True) 
    
    comando = "SELECT id_aviso, titulo, texto, data_aviso FROM AVISO ORDER BY data_aviso DESC"
    
    try:
        cursor.execute(comando)
        avisos = cursor.fetchall() # Agora 'avisos' é uma lista de dicionários
        
        # 3. Envia a lista de avisos (já em formato JSON) de volta para o front-end
        return jsonify(avisos), 200 # 200 = OK
        
    except mysql.connector.Error as err:
        return jsonify({"erro": f"Erro ao consultar avisos: {err}"}), 400
    
    finally:
        # Sempre feche o cursor e a conexão
        cursor.close()
        conexao.close()

# --- Rota para criar (que você já tinha) ---
@app.route('/api/criar_aviso', methods=['POST'])
def api_criar_aviso():
    # ... (seu código de criar aviso aqui) ...
    pass

# --- Inicia o Servidor ---
if __name__ == '__main__':
    app.run(debug=True)