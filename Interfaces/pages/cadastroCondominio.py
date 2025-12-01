import streamlit as st
from db_controller import get_db_connection, criar_condominio
import time

conexao = get_db_connection()
cursor = conexao.cursor()

st.set_page_config(page_title="Novo Condomínio")

st.title("Novo Condomínio")
st.markdown("Preencha os dados abaixo para registrar um novo condomínio.")

# Forms
with st.form("form_cadastro_condominio", height=600):
    st.subheader("Dados do Condomínio")
    nome = st.text_input("Nome do Condomínio*", placeholder="Ex: Residencial Flores")
    cnpj = st.text_input("CNPJ*", placeholder="Apenas números", max_chars=14)

    st.subheader("Endereço")
    c1, c2 = st.columns([3, 2])
    logradouro = c1.text_input("Logradouro*", placeholder="Rua, Avenida...")
    bairro = c2.text_input("Bairro*")

    c3, c4, c5 = st.columns([2, 1, 1])
    cidade = c3.text_input("Cidade*")
    uf = c4.text_input("UF*", placeholder="Ex: GO, DF", max_chars=2)
    cep = c5.text_input("CEP*", placeholder="Apenas números",  max_chars=8)

    submitted = st.form_submit_button("Salvar Cadastro", type="primary", use_container_width=True)
    cancelar = st.form_submit_button("Cancelar", use_container_width=True)

if cancelar:
    st.switch_page("pages/home.py")

# Salvando os dados
if submitted:
    if not nome or not cnpj:
        st.warning("Os campos **Nome** e **CNPJ** são obrigatórios.")
    if not cep or not cidade or not uf or not logradouro or not bairro:
        print("Os campos de endereço são obrigatórios!")
    else:
        cadastrar_condominio = criar_condominio(nome, cnpj, logradouro, bairro, cidade, uf, cep)
        
        if cadastrar_condominio:
            st.success(f"Condomínio **{nome}** cadastrado com sucesso")
            time.sleep(1.5) 
            st.switch_page("pages/home.py") 