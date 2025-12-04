import streamlit as st
import time
from db_functions import login_sessao, listar_moradores_residencia, criar_morador, editar_morador, deletar_morador, obter_residencia_por_id

st.set_page_config(page_title="Moradores", layout="centered")

login_sessao()

if 'detail_residencia' not in st.session_state:
    st.warning("Selecione uma residência primeiro.")
    st.stop()

residencia = st.session_state.detail_residencia
dados_residencia = obter_residencia_por_id(residencia)
moradores = listar_moradores_residencia(residencia)

if residencia:
    unidade, bloco, tipo, cnpj = residencia
    st.title(f"🏢 {unidade}")
    st.caption(f"{bloco}, {tipo}")


st.subheader("Unidades Cadastradas")
