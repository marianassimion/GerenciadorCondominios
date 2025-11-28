import streamlit as st
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME # Importa do config.py
from flask import Flask, make_response, jsonify, request


# CONEXÃO COM O BANCO DE DADOS
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

#FUNÇÕES
def criar_condominio(nome, cnpj, logradouro, bairro, cidade, uf, cep):
    comando = f'INSERT INTO condominio (nome, cnpj, logradouro, bairro, cidade, uf, cep) VALUES (%s, %s, %s, %s, %s, %s, %s)'
    valores = (nome, cnpj, logradouro, bairro, cidade, uf, cep)

    try:
        cursor.execute(comando, valores) # Executa o comando seguro
        conexao.commit()                 # Salva as alterações
        print(f"Condomínio '{nome}' criado com sucesso!")

    except mysql.connector.Error as err:
        print(f"Erro ao inserir condomínio: {err}")
        conexao.rollback() # Desfaz a operação em caso de erro

# INICIANDO INTERFACE
st.set_page_config (page_title = "Cadastro de condomínio", page_icon = ":tada:", layout="centered")
st.title("Cadastro de condomínio")
st.write("Preencha os campos abaixo")

with st.form(key='cadastro_form'):
    nome_input = st.text_input('Nome')
    cnpj_input = st.text_input('Cnpj')
    logradouro_input = st.text_input('Logradouro')
    bairro_input = st.text_input('Bairro')
    cidade_input = st.text_input('Cidade')
    uf_input = st.text_input('UF')
    cep_input = st.text_input('Cep')

    enviado = st.form_submit_button('Enviar')

if enviado:
    if not nome_input or not cnpj_input:
        st.error('Por favor, preencha os campos de nome e cnpj')
    
    else:
        nome = nome_input
        cnpj = cnpj_input
        logradouro = logradouro_input
        bairro = bairro_input
        cidade = cidade_input
        uf = uf_input
        cep = cep_input

    if criar_condominio(nome, cnpj, logradouro, bairro, cidade, uf, cep):
        st.success('Cadastro realizado com sucesso!')
    else:
        st.error('Erro ao cadastrar o condomínio.')
    
