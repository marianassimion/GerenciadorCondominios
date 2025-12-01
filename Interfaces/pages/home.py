import streamlit as st
from db_controller import *

# Conexão com o banco de dados
conexao = get_db_connection()
cursor = conexao.cursor()

login_sessao()

# Dados da sessão
admin_name = st.session_state.usuario[0]
admin_email = st.session_state.usuario[1] 

# CONDOMÍNIOS
with st.container(border=True):
    c1, c2, c3, c4 = st.columns([0.8, 4, 0.5, 0.5], vertical_alignment="center")
    c1.image("./img/user5.png", width=70)
    c2.markdown(f"**{admin_name}**\n<br><small>{admin_email}</small>", unsafe_allow_html=True)
    c4.button(":material/logout:", key="logout")

st.markdown("<div style='text-align: center; font-size: 24px;'>Condomínios</div>", unsafe_allow_html=True)
st.text_input("Buscar", placeholder="🔍 Digite o nome...", label_visibility="collapsed")
    
lista_condominios = listar_condominios()
    
with st.container(height=400, border=True):
    if not lista_condominios:
        st.info("Nenhum condomínio cadastrado")
            
    for cond in lista_condominios:
        cnpj_c, nome_c = cond[0], cond[1]
            
        with st.container(border=True):
            c_icon, c_nome, c_ver, c_edit, c_del = st.columns([0.5, 4, 0.5, 0.5, 0.5], vertical_alignment="center")
            c_icon.image("./img/apt2.png", width=70)
            c_nome.write(f"**{nome_c}**")
                
            if c_ver.button(":material/visibility:", key=f"ver_{cnpj_c}", help="Detalhes"):
                st.session_state['detail_cnpj'] = cnpj_c                
                st.switch_page("pages/detalharCondominio.py")
                st.rerun()
                
            if c_edit.button(":material/edit_square:", key=f"edit_{cnpj_c}", help="Editar condomínio"):
                st.session_state['cnpj_edicao'] = cnpj_c                
                st.switch_page("pages/edicaoCondominio.py")
                st.rerun()
                
            if c_del.button(":material/delete:", key=f"del_{cnpj_c}", help="Excluir condomínio"):
                if deletar_condominio(cnpj_c):
                    st.success("Condomínio excluído!") 
                    st.time.sleep(1)
                    st.rerun()
                    

if st.button("Cadastrar Novo Condomínio", type="primary", use_container_width=True):
    st.switch_page("pages/cadastroCondominio.py")