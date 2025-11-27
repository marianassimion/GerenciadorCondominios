import streamlit as st

# ------------ ADMINISTRADOR ------------

admin_name = "Nome do Administrador"
admin_email = "admin@exemplo.com"

lista_condominios = [
    {"id": 1, "nome": "Condominio Aguas Claras"},
    {"id": 2, "nome": "Condominio Asa Norte"},
    {"id": 3, "nome": "Condominio Asa Sul"},
    {"id": 4, "nome": "Condominio Lago Sul"},
    {"id": 5, "nome": "Condominio Sudoeste"},
    {"id": 6, "nome": "Condominio Noroeste"},       
]


# Painel do administrador
with st.container(border=True):
    col_icon, col_inf, col_editar, col_sair = st.columns([0.8, 4, 0.5, 0.5], vertical_alignment="center")

    # Imagem do usuário e informações do admin
    with col_icon:
        st.image("img/user5.png", width=70) 

    with col_inf:
        st.markdown(f"**{admin_name}**")
        st.caption(f"{admin_email}")

    # Botões de editar perfil e sair
    with col_editar:
        editar = st.button(":material/edit_square:", help="Editar perfil")

    with col_sair:
        sair = st.button(":material/logout:", help="Sair da conta")


# Painel de condomínios
with st.container(border=True):
    st.markdown("<div style='text-align: center; font-size: 24px;'>Condomínios</div>", unsafe_allow_html=True)
    st.write("") 

    barra_pesquisar = st.text_input("Buscar", placeholder="🔍 Digite o nome do condomínio...", label_visibility="collapsed")

    st.write("")

    # Lista de condomínios
    with st.container(height=300, border=False):
        for condominio in lista_condominios:
            with st.container(border=True):
                col_icon, col_nome, col_inf , col_editar, col_del = st.columns([0.5, 4, 0.5, 0.5, 0.5], vertical_alignment="center")
                
                # Icone do condomínio
                with col_icon:
                    st.image("img/condominio.png")
                    
                # Nome do condomínio
                with col_nome:
                    st.write(f"**{condominio['nome']}**")

                # Botões de visualizar, editar e excluir
                with col_inf:
                    st.button(":material/visibility:", key=f"btn_info_{condominio['id']}", help="Mais informações")
                with col_editar:
                    st.button(":material/edit_square:", key=f"btn_edit_{condominio['id']}", help="Editar condomínio")

                with col_del:
                    st.button(":material/delete:", key=f"btn_del_{condominio['id']}", help="Excluir condomínio")

# Botão de cadastro de condomínio
cadastrar_condominio = st.button("Cadastrar +", help="Cadastrar novo condomínio", use_container_width=True)