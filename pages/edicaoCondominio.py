import streamlit as st
import time
from src.db_functions import obter_condominio_por_cnpj, atualizar_condominio

st.set_page_config(page_title="Editar Condomínio")

def voltar_home():
    if 'cnpj_edicao' in st.session_state:
        del st.session_state['cnpj_edicao']
    st.switch_page("pages/home.py") 

if 'cnpj_edicao' not in st.session_state or st.session_state.cnpj_edicao is None:
    st.warning("Nenhum condomínio selecionado para edição.")
    if st.button("Voltar para Home"):
        voltar_home()
    st.stop()

cnpj_atual = st.session_state.cnpj_edicao

if st.button("Cancelar e Voltar"):
    voltar_home()

st.title("Editar Condomínio")

dados = obter_condominio_por_cnpj(cnpj_atual)

if dados:
    nome_atual, log_atual, bairro_atual, cid_atual, uf_atual, cep_atual = dados

   # Forms
    with st.form("form_editar_condominio", clear_on_submit=False):
        st.caption(f"Editando dados do CNPJ: {cnpj_atual}")
        
        novo_nome = st.text_input("Nome", value=nome_atual, key="input_nome")
        st.text_input("CNPJ", value=cnpj_atual, disabled=True, key="input_cnpj")

        st.subheader("Endereço")
        c1, c2 = st.columns([3, 2])
        novo_log = c1.text_input("Logradouro", value=log_atual, key="input_log")
        novo_bairro = c2.text_input("Bairro", value=bairro_atual, key="input_bairro")

        c3, c4, c5 = st.columns([2, 1, 1])
        nova_cid = c3.text_input("Cidade", value=cid_atual, key="input_cid")
        nova_uf = c4.text_input("UF", value=uf_atual, max_chars=2, key="input_uf")
        novo_cep = c5.text_input("CEP", value=cep_atual, key="input_cep")

        salvar = st.form_submit_button("Salvar Alterações", type="primary", use_container_width=True)

    # Salvando edição do Condomínio
    if salvar:
        if not novo_nome:
            st.warning("O nome não pode ficar vazio.")
        else:
            try:
                sucesso = atualizar_condominio(cnpj_atual, novo_nome, novo_log, novo_bairro, nova_cid, nova_uf, novo_cep)
                
                if sucesso:
                    st.success("Condomínio atualizado com sucesso! Redirecionando...")
                    time.sleep(1.5) 
                    voltar_home()   
                else:
                    st.error("Erro ao atualizar no banco de dados. Tente novamente.")
            
            except Exception as e:
                st.error(f"Ocorreu um erro técnico: {e}")

else:
    st.error(f"Não foi possível encontrar os dados para o CNPJ {cnpj_atual}.")
    if st.button("Voltar"):
        voltar_home()