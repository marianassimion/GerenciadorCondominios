import streamlit as st
import time
from db_functions import login_sessao, criar_residencia

st.set_page_config(page_title="Nova Residência", layout="centered")

login_sessao()

if 'detail_cnpj' not in st.session_state:
    st.warning("Selecione um condomínio primeiro.")
    st.stop()
    
cnpj = st.session_state.detail_cnpj

st.title("Nova Residência")
st.markdown(f"Preencha os dados da unidade para o condomínio atual.")

# Forms
with st.form("form_cadastro_residencia", height=300):
    st.subheader("Dados da Unidade")
    
    c1, c2 = st.columns([1, 1])
    num_unidade = c1.number_input("Número da Unidade*", min_value=1, step=1, placeholder="Ex: 101")
    bloco = c2.text_input("Bloco*", placeholder="Ex: Bloco A")

    tipo = st.selectbox("Tipo de Imóvel*", ["Apartamento", "Casa", "Cobertura", "Studio"])

    col_b1, col_b2 = st.columns([1, 1])
    enviado = col_b1.form_submit_button("Salvar Residência", type="primary", use_container_width=True)
    cancelar = col_b2.form_submit_button("Cancelar", use_container_width=True)

if cancelar:
    st.switch_page("pages/residencias.py") 

# Salvando nova Residência
if enviado:
    if not num_unidade:
        st.warning("O campo **Número da Unidade** é obrigatório.")
    else:
        sucesso = criar_residencia(num_unidade, bloco, tipo, cnpj)
        
        if sucesso:
            st.success(f"Residência **{num_unidade} - {bloco}** cadastrada com sucesso!")
            time.sleep(1.5)
            st.switch_page("pages/residencias.py") 
        else:
            st.error("Não foi possível realizar o cadastro!")

