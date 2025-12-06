import streamlit as st
import time
from src.db_functions import login_sessao, criar_veiculo

st.set_page_config(page_title="Novo Veículo", layout="centered")

login_sessao()

if 'detail_residencia' not in st.session_state:
    st.warning("Selecione uma residência.")
    st.stop()
    
id_residencia = st.session_state.detail_residencia
cpf_morador = st.session_state.veiculo_morador

st.title("Novo Veículo")
st.markdown(f"Preencha os dados")

# Forms
with st.form(key='cadastro_veiculo_form'):
    placa  = st.text_input('Placa*', max_chars=7)
    modelo = st.text_input('Modelo*', max_chars=40)
    cor = st.text_input("Cor", max_chars=20)

    b1, b2 = st.columns(2)
    with b1:
        cancelar = st.form_submit_button('Cancelar', use_container_width=True)
    with b2:
        enviado = st.form_submit_button('Salvar Cadastro', type="primary", use_container_width=True)

if cancelar:   
    st.switch_page("pages/listagemVeiculoResidencia.py")

# Salvando novo Veículo
if enviado:
    if not placa or not modelo or not cor:
        st.warning("Por favor, preencha a data de emissão, a data de vencimento e a cor")
    else:
        
        veiculo = criar_veiculo(placa, modelo, cor, cpf_morador)

        if veiculo:
            st.success(f"Veículo {placa} cadastrado com sucesso!")
            time.sleep(1.5)
            
            if 'details_condominio_mode' in st.session_state:
                st.session_state.details_condominio_mode = True
                
            st.switch_page("pages/listagemVeiculoResidencia.py")
        else:
            st.error("Erro ao cadastrar veiculo. Verifique os dados.")