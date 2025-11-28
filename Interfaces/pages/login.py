import streamlit as st

# ------------ LOGIN ------------

# Configurações da página
st.set_page_config(page_title="Login", layout="centered")

def login_page():
    
    # Imagem do usuário e título
    col1, col2, col3 = st.columns([1, 0.3, 1])
    with col2:
        st.image("../img/user4.png", width=90)

    st.markdown("<div style='text-align: center; font-size: 24px;'>Administrador</div>", unsafe_allow_html=True)

    # Inputs
    email = st.text_input("Email", placeholder="usuario@gmail.com", key="input_email", help="Digite seu email")
    senha = st.text_input("Senha", placeholder="senha", type="password", key="input_senha", help="Digite sua senha")

    # Link de esqueceu a senha
    st.markdown('<div  style="text-align: center; font-size: 17px; padding: 15px;" class="forgot-password"><a href="#">Esqueceu a senha?</a></div>', unsafe_allow_html=True)

    # Botão de login 
    col1, col_login, col3 = st.columns([1, 0.3, 1], vertical_alignment="center")
    with col_login:
        login = st.button("Entrar")

    # Lógica de autenticação (implementar a verificação dos dados de login no banco de dados)
    if login:
        st.switch_page("pages/home.py")

    st.markdown('</div>', unsafe_allow_html=True)

login_page()



