import streamlit as st
from db_functions import criar_condominio
import time

st.set_page_config(page_title="Novo Condomínio")

# Título
st.title("Novo Condomínio")
st.markdown("Preencha os dados abaixo para registrar um novo condomínio.")

# Botão de Voltar
if st.button("Voltar para Listagem"):
    st.switch_page("home.py")

# --- FORMULÁRIO ---
with st.form("form_cadastro_condominio"):
    st.subheader("Dados Principais")
    nome = st.text_input("Nome do Condomínio", placeholder="Ex: Residencial Flores")
    cnpj = st.text_input("CNPJ", placeholder="Apenas números", max_chars=14)

    st.subheader("Endereço")
    c1, c2 = st.columns([3, 2])
    logradouro = c1.text_input("Logradouro", placeholder="Rua, Avenida...")
    bairro = c2.text_input("Bairro")

    c3, c4, c5 = st.columns([2, 1, 1])
    cidade = c3.text_input("Cidade")
    uf = c4.text_input("UF", max_chars=2)
    cep = c5.text_input("CEP")

    # Botão de Enviar
    submitted = st.form_submit_button("Salvar Cadastro", type="primary", use_container_width=True)

# ---  SALVAR ---
if submitted:
    # 1. Validação simples
    if not nome or not cnpj:
        st.warning("Os campos **Nome** e **CNPJ** são obrigatórios.")
    
    else:
        # 2. Tenta salvar no banco
        sucesso = criar_condominio(nome, cnpj, logradouro, bairro, cidade, uf, cep)
        
        if sucesso:

            st.success(f"✅ Condomínio **{nome}** cadastrado com sucesso!")
            
            # 3. Redirecionar após sucesso
            time.sleep(1.5) # Espera 1.5s para o usuário ler a mensagem
            st.switch_page("home.py") # Volta para a página principal automaticamente