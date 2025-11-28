import streamlit as st
import mysql.connector
from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER

#=============================================
# CONEXÃO COM O BANCO DE DADOS
#=============================================

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
    st.error(f"Erro ao conectar no MySQL: Verifique as configurações no config.py. Erro: {err}")
    #interromper a execução do Streamlit
    st.stop()


# =========================================================================
# VARIÁVEIS E FUNÇÕES DE GESTÃO DE DADOS
# =========================================================================

admin_name = "Nome do Administrador"
admin_email = "admin@exemplo.com"
