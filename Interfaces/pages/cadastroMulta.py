import streamlit as st
import time
from db_functions import login_sessao, criar_multa

st.set_page_config(page_title="Nova Multa", layout="centered")

login_sessao()

if 'detail_residencia' not in st.session_state:
    st.warning("Selecione uma residência.")
    st.stop()
    
id_residencia = st.session_state.detail_residencia

st.title("Nova Multa")
st.markdown(f"Preencha os dados")

# Forms
with st.form(key='cadastro_multa_form'):
    data_emissao = st.date_input('Data de Emissão*')
    data_vencimento = st.date_input('Data de Vencimento*')
    valor = st.number_input('Valor*', min_value=0.0, step=10.0)
    status = st.selectbox('Status*', ['Pendente', 'Pago', 'Atrasado'])
    descricao = st.text_area('Descrição', height=100)

    b1, b2 = st.columns(2)
    with b1:
        cancelar = st.form_submit_button('Cancelar', use_container_width=True)
    with b2:
        enviado = st.form_submit_button('Salvar Cadastro', type="primary", use_container_width=True)

if cancelar:   
    st.switch_page("pages/listagemTaxasMultas.py")

# Salvando nova Multa
if enviado:
    if not data_emissao or not data_vencimento:
        st.warning("Por favor, preencha a data de emissão e a data de vencimento.")
    else:
        
        taxa = criar_multa(data_emissao, data_vencimento, status, valor, descricao, id_residencia)

        if taxa:
            st.success(f"Taxa cadastrada com sucesso!")
            time.sleep(1.5)
            
            if 'details_condominio_mode' in st.session_state:
                st.session_state.details_condominio_mode = True
                
            st.switch_page("pages/listagemTaxasMultas.py")
        else:
            st.error("Erro ao cadastrar multa. Verifique os dados.")