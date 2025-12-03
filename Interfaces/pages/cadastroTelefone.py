import streamlit as st
import time
from db_functions import login_sessao, criar_telefone, obter_morador_por_id

st.set_page_config(page_title="Novo Telefone", layout="centered")

login_sessao()

if 'morador_phone' not in st.session_state:
    st.warning("Selecione um morador.")
    st.stop()
    
cpf_morador = st.session_state.morador_phone

morador = obter_morador_por_id(cpf_morador)
nome = morador[1] 

st.title("Novo telefone")
st.subheader(f"Morador: **{nome}**")

# FORMULÁRIO
with st.form(key='cadastro_telefone_form'):
    telefone = st.text_input('Telefone*', placeholder="Ex: 61999999999", max_chars=11)
    
    b1, b2 = st.columns(2)
    with b1:
        cancelar = st.form_submit_button('Cancelar', use_container_width=True)
    with b2:
        enviado = st.form_submit_button('Salvar Cadastro', type="primary", use_container_width=True)


if cancelar:   
    st.switch_page("pages/moradorResidencia.py")

# SALVANDO TELEFONE
if enviado:
    if not telefone:
        st.warning("Por favor, preencha o número de telefone.")
    else:
        sucesso = criar_telefone(cpf_morador, telefone) 
        
        if sucesso:
            st.success(f"Telefone {telefone} cadastrado para {nome} com sucesso!")
            
            if 'details_condominio_mode' in st.session_state:
                st.session_state.details_condominio_mode = True
            
            time.sleep(1.5)
            st.switch_page("pages/moradorResidencia.py")
        else:
            st.error("Erro ao salvar no banco de dados.")