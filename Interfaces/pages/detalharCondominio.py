import streamlit as st
import time
from db_functions import login_sessao, obter_condominio_por_cnpj, obter_empregados, deletar_empregado

st.set_page_config(page_title="Detalhes do Condomínio")

login_sessao()

if 'detail_cnpj' not in st.session_state or st.session_state.detail_cnpj is None:
    st.warning("Nenhum condomínio selecionado para edição.")
    if st.button("Voltar para Home"): 
        st.switch_page("pages/home.py")
    st.stop() # Para a execução

cnpj_atual = st.session_state.detail_cnpj

if st.button("Voltar para Home"):
    st.switch_page("pages/home.py")


dados_condominio = obter_condominio_por_cnpj(cnpj_atual)

if dados_condominio:
    nome, log, bai, cid, uf, cep = dados_condominio
    
    # Cabeçalho do Condomínio
    st.title(f"🏢 {nome}")
    st.caption(f"{log}, {bai} - {cid}/{uf} | CEP: {cep}")
    st.caption(f"CNPJ: {cnpj_atual}")
    st.divider()

    # --- SEÇÃO DE AVISOS ---
    c_avisos, c_empregados, c_areas = st.columns([1.5, 1.5,1.5], vertical_alignment="bottom")

    if c_avisos.button("Quadro de avisos", use_container_width=True):
        st.switch_page("pages/listagemAvisos.py")

    if c_empregados.button("Quadro de Funcionários", use_container_width=True):
        st.switch_page("pages/listagemEmpregados.py")

    if c_areas.button("Áreas comuns", use_container_width=True):
                st.switch_page("pages/listagemAreasComuns.py")

else:
    st.error("Erro ao carregar dados do condomínio.")