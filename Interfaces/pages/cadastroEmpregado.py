import streamlit as st
import time
from db_functions import criar_empregado, obter_condominio_por_cnpj, login_sessao

st.set_page_config(page_title="Novo Empregado")

login_sessao()

if 'detail_cnpj' not in st.session_state or st.session_state.detail_cnpj is None:
    st.warning("Nenhum condomínio selecionado.")
    st.button("Voltar para Home", on_click=lambda: st.switch_page("page/listagemEmpregados.py"))
    st.stop()


cnpj_atual = st.session_state.detail_cnpj
dados_condo = obter_condominio_por_cnpj(cnpj_atual)
nome_condominio = dados_condo[0] if dados_condo else "Não identificado"

st.title("Novo Colaborador")
st.write(f"Cadastrando funcionário no condomínio: **{nome_condominio}**")
st.caption(f"CNPJ: {cnpj_atual}")

# FORMULÁRIO
with st.form(key='cadastro_empregado_form'):
    nome = st.text_input('Nome Completo')
    
    c1, c2 = st.columns(2)
    cpf = c1.text_input('CPF (apenas números)', max_chars=11)
    cargo = c2.text_input('Cargo')
    
    c3, c4, c5 = st.columns(3)
    matricula = c3.text_input('Matrícula')
    data_admissao = c4.date_input('Data de Admissão')
    salario = c5.number_input('Salário', min_value=0.0, step=100.0)
    
    enviado = st.form_submit_button('Salvar Cadastro', type="primary", use_container_width=True)
    cancelar = st.form_submit_button('Cancelar', use_container_width=True)

if cancelar:   
    st.switch_page("pages/listagemEmpregados.py")

# SALVANDO EMPREGADO
if enviado:
    if not nome or not cpf:
        st.error('Os campos **Nome** e **CPF** são obrigatórios.')
    else:
        cpf_limpo = cpf.replace(".", "").replace("-", "")
        
        if len(cpf_limpo) > 11:
            st.error("CPF inválido (muitos dígitos).")
        else:
            sucesso = criar_empregado(cpf_limpo, nome, cargo, matricula, data_admissao, salario, cnpj_atual)
            
            if sucesso:
                st.success(f"Funcionário **{nome}** cadastrado com sucesso!")
                time.sleep(1.5)
                st.session_state.details_condominio_mode = True
                st.switch_page("pages/home.py")