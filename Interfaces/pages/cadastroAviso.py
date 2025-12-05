import streamlit as st
from db_functions import criar_aviso, obter_condominio_por_cnpj, login_sessao
import time

st.set_page_config(page_title="Novo Aviso", layout="centered")

login_sessao()

id_administrador = st.session_state.usuario[0]

if 'detail_cnpj' not in st.session_state or st.session_state.detail_cnpj is None:
    st.warning("Nenhum condomínio selecionado.")
    st.button("Voltar para Home", on_click=lambda: st.switch_page("home.py"))
    st.stop()

cnpj_atual = st.session_state.detail_cnpj
dados_condo = obter_condominio_por_cnpj(cnpj_atual)
nome_condominio = dados_condo[0] if dados_condo else "Não identificado"

st.title("Novo aviso")
st.write(f"Cadastrando aviso para o condomínio: **{nome_condominio}**")

# Forms
with st.form(key='cadastro_aviso_form'):
    titulo = st.text_input('Título')
    texto = st.text_area('Texto', height=150)
    
    enviado = st.form_submit_button('Postar aviso', type="primary", use_container_width=True)
    cancelar = st.form_submit_button('Cancelar', use_container_width=True)

if cancelar:
    st.switch_page("pages/listagemAvisos.py")

# Salvando novo Aviso
if enviado:
    print(titulo, texto, id_administrador, cnpj_atual)
    if not titulo:
        st.error('O aviso deve ter um título')
    elif not texto:
        st.error('O aviso não pode estar vazio') 
    else:
        sucesso = criar_aviso(titulo, texto, id_administrador, cnpj_atual)
        if sucesso:
            st.success("Aviso publicado com sucesso!")
            time.sleep(1.5)
            st.switch_page("pages/listagemAvisos.py")
        