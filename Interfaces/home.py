import streamlit as st
import mysql.connector
from db_functions import get_db_connection, deletar_condominio, listar_condominios, deletar_condominio, obter_condominio_por_cnpj
# =========================================================================
# 1. CONFIGURAÇÃO E CONEXÃO COM BANCO DE DADOS
# =========================================================================

conexao = get_db_connection()
cursor = conexao.cursor()

admin_name = "Admin"
admin_email = "admin@sistema.com"

# ------------------ 5. LISTAGEM PRINCIPAL (DEFAULT) ------------------
with st.container(border=True):
    c1, c2, c3, c4 = st.columns([0.8, 4, 0.5, 0.5], vertical_alignment="center")
    c1.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=50)
    c2.markdown(f"**{admin_name}**\n<br><small>{admin_email}</small>", unsafe_allow_html=True)
    c4.button(":material/logout:", key="logout")

    # Lista
st.title("Condomínios")
st.text_input("Buscar", placeholder="Digite o nome...", label_visibility="collapsed")
    
lista = listar_condominios()
    
with st.container(height=400, border=False):
    if not lista:
        st.info("Nenhum condomínio encontrado.")
            
    for cond in lista:
        cnpj_c, nome_c = cond[0], cond[1]
            
        with st.container(border=True):
            c_icon, c_nome, c_ver, c_edit, c_del = st.columns([0.5, 4, 0.5, 0.5, 0.5], vertical_alignment="center")
            c_icon.write("🏢")
            c_nome.write(f"**{nome_c}**")
                
            if c_ver.button(":material/visibility:", key=f"ver_{cnpj_c}"):
                st.session_state['detail_cnpj'] = cnpj_c                
                st.switch_page("pages/detalharCondominio.py")
                st.rerun()
                
            if c_edit.button(":material/edit_square:", key=f"edit_{cnpj_c}"):
                st.session_state['cnpj_edicao'] = cnpj_c                
                st.switch_page("pages/edicaoCondominio.py")
                st.rerun()
                
            if c_del.button(":material/delete:", key=f"del_{cnpj_c}"):
                if deletar_condominio(cnpj_c):
                    st.success("Condomínio excluído!") #corrgir tamanho
                    st.time.sleep(1)
                    st.rerun()
                    

    st.write("---")
    if st.button("Cadastrar Novo Condomínio", type="primary", use_container_width=True):
        st.switch_page("pages/cadastroCondominio.py")