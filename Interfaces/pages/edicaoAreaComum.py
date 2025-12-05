import streamlit as st
import time
from db_functions import obter_area_comum, atualizar_area_comum

st.set_page_config(page_title="Editar Área Comum", layout="centered")

if 'editing_area_comum' not in st.session_state or st.session_state.editing_area_comum is None:
    st.warning("Nenhuma área comum selecionada para edição.")
    if st.button("Voltar para Listagem"):
        st.switch_page("pages/listagemAreasComuns.py")
    st.stop()

area_comum_atual = st.session_state.editing_area_comum

if st.button("Cancelar e Voltar"):
    st.session_state.details_condominio_mode = True 
    st.switch_page("pages/listagemAreasComuns.py")

st.title("Editar Área Comum")

dados = obter_area_comum(area_comum_atual)

if dados:
    nome_at, desc_at, cap_at = dados[0]

    #Forms
    with st.form("form_editar_area_comum"):
        st.caption(f"Editando área comum (Nome: {nome_at})")
        
        nome = st.text_input("Nome", value=nome_at)
        descricao = st.text_input("Descrição", value=desc_at) 
        capacidade = st.number_input("Capacidade", value=cap_at, min_value=1, step=1)
        salvar = st.form_submit_button("Salvar Alterações", type="primary", use_container_width=True)


    # Salvando edição da Área Comum
    if salvar:
        if not nome:
            st.error("O nome é obrigatório.")
        else:
            sucesso = atualizar_area_comum(area_comum_atual,nome, descricao, capacidade)
            
            if sucesso:
                st.success("Dados atualizados com sucesso!")
                time.sleep(1)
                st.session_state.details_condominio_mode = True 
                st.switch_page("pages/listagemAreasComuns.py")
else:
    st.error("Área comum não encontrada.")