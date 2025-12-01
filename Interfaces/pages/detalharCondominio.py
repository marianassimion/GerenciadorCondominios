import streamlit as st
import time
from db_functions import obter_condominio_por_cnpj, obter_empregados, deletar_empregado

st.set_page_config(page_title="Detalhes do Condomínio")

if 'detail_cnpj' not in st.session_state or st.session_state.detail_cnpj is None:
    st.warning("Nenhum condomínio selecionado para edição.")
    if st.button("Voltar para Home"): 
        st.switch_page("pages/home.py")
    st.stop() # Para a execução

# Pegamos o CNPJ da memória
cnpj_atual = st.session_state.detail_cnpj

if st.button("Voltar para Home"):
    st.switch_page("pages/home.py")


dados_condominio = obter_condominio_por_cnpj(cnpj_atual)
empregados = obter_empregados(cnpj_atual)

if dados_condominio:
    nome, log, bai, cid, uf, cep = dados_condominio
    
    # Cabeçalho do Condomínio
    st.title(f"🏢 {nome}")
    st.caption(f"{log}, {bai} - {cid}/{uf} | CEP: {cep}")
    st.caption(f"CNPJ: {cnpj_atual}")
    st.divider()

    # --- SEÇÃO DE AVISOS ---
    col_tit, col_btn = st.columns([3, 1], vertical_alignment="bottom")
    if col_btn.button("Quadro de avisos", use_container_width=True):
        st.switch_page("pages/listagemAvisos.py")

    # --- SEÇÃO DE EMPREGADOS ---
    col_tit, col_btn = st.columns([3, 1], vertical_alignment="bottom")
    if col_btn.button("Quadro de Funcionários", use_container_width=True):
        # Redireciona para a página de cadastro de empregado
        st.switch_page("pages/listagemEmpregados.py")
    
    
else:
    st.error("Erro ao carregar dados do condomínio.")