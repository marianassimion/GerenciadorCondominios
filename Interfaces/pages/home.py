import streamlit as st
from db_functions import *
import time

st.set_page_config(page_title="Condomínios", layout="centered")

@st.dialog("Confirmar Exclusão")
def confirmar_exclusao(cnpj):
    st.warning(f"Tem certeza que deseja excluir esse condomínio?")
    st.write("⚠️ Esta ação é irreversível e afetará todas as residências e moradores associados.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Sim, excluir", type="primary"):
            sucesso = deletar_condominio(cnpj)
            if sucesso:
                st.success("Condomínio excluído com sucesso!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Erro ao excluir condomínio.")
    with col2:
        if st.button("Cancelar"):
            st.rerun()


if "usuario" not in st.session_state:
    st.switch_page("login.py") 

admin_id = st.session_state.usuario[0]
admin_name = st.session_state.usuario[1]
admin_email = st.session_state.usuario[2] 

with st.container(border=True):
    c1, c2, c3, c4 = st.columns([0.8, 4, 0.5, 0.5], vertical_alignment="center")
    c1.image("./img/user5.png", width=70)
    c2.markdown(f"**{admin_name}**\n<br><small>{admin_email}</small>", unsafe_allow_html=True)

    if c4.button(":material/logout:", key="logout", help="Sair do sistema"):
        st.session_state.clear()      
        st.switch_page("login.py")    

st.markdown("<div style='text-align: center; font-size: 24px;'>Condomínios</div>", unsafe_allow_html=True)
    
lista_condominios = listar_condominios(admin_id)
    
with st.container(height=400, border=True):
    if not lista_condominios:
        st.info("Nenhum condomínio cadastrado para este administrador.")
            
    for cond in lista_condominios:
        cnpj_c = cond[0]
        nome_c = cond[2]
            
        with st.container(border=True):
            cols = st.columns([0.5, 4, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8], vertical_alignment="center")
            
            cols[0].image("./img/apt2.png", width=70)
            cols[1].write(f"**{nome_c}**")
                
            if cols[2].button(":material/visibility:", key=f"ver_{cnpj_c}", help="Detalhes"):
                st.session_state['detail_cnpj'] = cnpj_c                
                st.switch_page("pages/detalharCondominio.py")
            
            if cols[3].button(":material/home_work:", key=f"res_{cnpj_c}", help="Residências"):
                st.session_state['detail_cnpj'] = cnpj_c                
                st.switch_page("pages/residencias.py")

            if cols[4].button(":material/perm_identity:", key=f"mor_{cnpj_c}", help="Moradores"):
                st.session_state['detail_cnpj'] = cnpj_c                
                st.switch_page("pages/moradorCondominio.py")

            if cols[5].button(":material/directions_car:", key=f"car_{cnpj_c}", help="Veículos"):
                st.session_state['detail_cnpj'] = cnpj_c                
                st.switch_page("pages/veiculoCondominio.py")

            if cols[6].button(":material/edit_square:", key=f"edit_{cnpj_c}", help="Editar"):
                st.session_state['cnpj_edicao'] = cnpj_c                
                st.switch_page("pages/edicaoCondominio.py")
                
            if cols[7].button(":material/delete:", key=f"del_{cnpj_c}", help="Excluir"):
                confirmar_exclusao(cnpj_c)

if st.button("Cadastrar Novo Condomínio", type="primary", use_container_width=True):
    st.switch_page("pages/cadastroCondominio.py")