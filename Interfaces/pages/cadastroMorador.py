import streamlit as st
import time
from db_functions import login_sessao, criar_morador, criar_telefone

st.set_page_config(page_title="Novo Morador", layout="centered")

login_sessao()

if 'detail_residencia' not in st.session_state:
    st.warning("Selecione uma residência.")
    st.stop()
    
id_residencia = st.session_state.detail_residencia

st.title("Novo Morador")
st.markdown(f"Preencha os dados do novo morador")

# FORMULÁRIO
with st.form(key='cadastro_morador_form'):
    nome = st.text_input('Nome*')
    
    c1, c2 = st.columns(2)
    cpf = c1.text_input('CPF*', placeholder="Apenas números", max_chars=11)
    email = c2.text_input('Email*')
    
    c3, c4 = st.columns(2)
    s = c3.selectbox("Síndico*", ["Sim", "Não"])
    telefone = c4.text_input('Telefone*', placeholder="Apenas números", max_chars=11)
    
    b1, b2 = st.columns(2)
    with b1:
        cancelar = st.form_submit_button('Cancelar', use_container_width=True)
    with b2:
        enviado = st.form_submit_button('Salvar Cadastro', type="primary", use_container_width=True)

if cancelar:   
    st.switch_page("pages/moradorResidencia.py")

# SALVANDO MORADOR E TELEFONE
if enviado:
    if not nome or not cpf:
        st.warning("Por favor, preencha o Nome e o CPF.")
    else:
        morador_sindico = True if s == "Sim" else False
        
        morador_criado = criar_morador(cpf, nome, email, id_residencia, morador_sindico)
        
        if morador_criado and telefone:
            telefone_criado = criar_telefone(cpf, telefone) 

        if morador_criado and telefone_criado:
            st.success(f"Morador **{nome}** cadastrado com sucesso!")
            time.sleep(1.5)
            
            if 'details_condominio_mode' in st.session_state:
                st.session_state.details_condominio_mode = True
                
            st.switch_page("pages/moradorResidencia.py")
        else:
            st.error("Erro ao cadastrar morador ou telefone. Verifique os dados.")