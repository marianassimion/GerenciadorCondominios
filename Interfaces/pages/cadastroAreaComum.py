import streamlit as st
from db_functions import criar_area_comum, obter_condominio_por_cnpj, login_sessao
import time

login_sessao()

# Pegar o id do administrador
id_administrador = st.session_state.usuario[0]

if 'detail_cnpj' not in st.session_state or st.session_state.detail_cnpj is None:
    st.warning("Nenhum condomínio selecionado.")
    st.button("Voltar para Home", on_click=lambda: st.switch_page("pages/home.py"))
    st.stop()

cnpj_atual = st.session_state.detail_cnpj
dados_condo = obter_condominio_por_cnpj(cnpj_atual)
nome_condominio = dados_condo[0] if dados_condo else "Não identificado"

st.title("Nova área comum")
st.write(f"Cadastrando nova área comum para o condomínio: **{nome_condominio}**")

with st.form(key='cadastro_area_comum_form'):
    nome = st.text_input('Nome')
    descricao = st.text_area('Descrição', height=60)
    capacidade = st.number_input('Capacidade', min_value=1, step=1)

    enviado = st.form_submit_button('Adicionar área comum', type="primary", use_container_width=True)
    cancelar = st.form_submit_button('Cancelar', use_container_width=True)

if cancelar:
    st.switch_page("pages/listagemAvisos.py")

if enviado:
    if not nome:
        st.error('A área comum deve ter um título')
    elif not descricao:
        st.error('A área comum não pode estar vazio') 
    else:
        sucesso = criar_area_comum(nome, descricao, capacidade, cnpj_atual)
        if sucesso:
            st.success("Área comum criada com sucesso!")
            time.sleep(1.5)
            st.switch_page("pages/listagemAreasComuns.py")
        