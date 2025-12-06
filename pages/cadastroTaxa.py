import streamlit as st
import time
from src.db_functions import login_sessao, criar_taxa

st.set_page_config(page_title="Nova Taxa", layout="centered")

login_sessao()

if 'detail_residencia' not in st.session_state:
    st.warning("Selecione uma residência.")
    st.stop()
    
id_residencia = st.session_state.detail_residencia

st.title("Nova Taxa")
st.markdown(f"Preencha os dados")

# Forms
with st.form(key='cadastro_taxa_form'):
    data_emissao = st.date_input('Data de Emissão*')
    data_vencimento = st.date_input('Data de Vencimento*')
    valor = st.number_input('Valor*', min_value=0.0, step=10.0)
    status = st.selectbox('Status*', ['Pendente', 'Pago', 'Atrasado'])

    b1, b2 = st.columns(2)
    with b1:
        cancelar = st.form_submit_button('Cancelar', use_container_width=True)
    with b2:
        enviado = st.form_submit_button('Salvar Cadastro', type="primary", use_container_width=True)

if cancelar:   
    st.switch_page("pages/listagemTaxasMultas.py")

# Salvando nova Taxa
if enviado:
    if not data_emissao or not data_vencimento:
        st.warning("Por favor, preencha a data de emissão e a data de vencimento.")
    else:
        
        taxa = criar_taxa(data_emissao, data_vencimento, valor, status, id_residencia)

        if taxa:
            st.success(f"Taxa cadastrada com sucesso!")
            time.sleep(1.5)
            
            if 'details_condominio_mode' in st.session_state:
                st.session_state.details_condominio_mode = True
                
            st.switch_page("pages/listagemTaxasMultas.py")
        else:
            st.error("Erro ao cadastrar taxa. Verifique os dados.")