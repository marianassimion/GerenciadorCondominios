import streamlit as st
import time
from db_functions import verificar_login 

# ------------ LOGIN ------------
st.set_page_config(page_title="Login", layout="centered")

def login_page():    
    col1, col2, col3 = st.columns([1, 0.3, 1])
    with col2:
        st.image("img/user4.png", width=90)

    st.markdown("<div style= font-size: 24px;'>Endereço</div>", unsafe_allow_html=True)

    email = st.text_input("Email", placeholder="usuario@gmail.com", key="input_email", help="Digite seu email")
    senha = st.text_input("Senha", placeholder="senha", type="password", key="input_senha", help="Digite sua senha")

    col1, col_login, col3 = st.columns([1, 0.3, 1], vertical_alignment="center")
    with col_login:
        login = st.button("Entrar")

    # Lógica de autenticação
    if login:
        if not email or not senha:
            st.warning("Preencha todos os campos!")
        else:
            usuario = verificar_login(email, senha)
            
            if usuario:
                st.session_state.logged_in = True
                st.session_state.usuario = usuario
                
                st.success("Login realizado com sucesso!")
                time.sleep(0.5) 

                # Redireciona para Home
                st.switch_page("pages/home.py") 
            else:
                st.error("E-mail ou senha incorretos")

    st.markdown('</div>', unsafe_allow_html=True)

login_page()



