import streamlit as st
import time
from src.db_functions import obter_morador_por_id, editar_morador, editar_telefone, obter_telefone_por_cpf

st.set_page_config(page_title="Editar Morador", layout="centered")


if 'morador_edit' not in st.session_state:
    st.warning("Nenhum morador selecionado para edição.")
    st.stop()

cpf = st.session_state.morador_edit

st.title("Editar Morador")

dados_morador = obter_morador_por_id(cpf)
dados_telefone = obter_telefone_por_cpf(cpf) 

if dados_morador:
    cpf_morador, nome, email, id_res, sindico = dados_morador

    id_tel_db = dados_telefone[0] if dados_telefone else None
    num_tel_db = dados_telefone[1] if dados_telefone else ""


    # Forms
    with st.form("form_editar_morador"):
        st.caption(f"Editando cadastro (CPF: {cpf_morador})")

        st.subheader("Dados Pessoais")
        
        novo_nome = st.text_input("Nome Completo", value=nome)
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("CPF", value=cpf, disabled=True)
        with col2:
            novo_email = st.text_input("E-mail", value=email)

        st.divider()
        st.subheader("Informações Residenciais")
        
        col3, col4 = st.columns(2)
        with col3:
            novo_id_residencia = st.text_input("ID Residência", value= id_res, disabled=True)
        with col4:
            novo_sindico = st.checkbox("É Síndico?", value=bool(sindico))

        st.divider()
        st.subheader("Contato")
        novo_telefone = st.text_input("Telefone", value=num_tel_db, max_chars=11)

        salvar = st.form_submit_button("Salvar Alterações", type="primary", use_container_width=True)
        cancelar = st.form_submit_button("Cancelar", use_container_width=True)

    if cancelar:
        st.session_state.morador_edit= None
        st.switch_page("pages/listagemMoradorResidencia.py") 


    # Salvando edições do Morador
    if salvar:
        erro_validacao = False
        
        if not novo_nome:
            st.error("O nome é obrigatório.")
            erro_validacao = True
        if not novo_email:
            st.error("O e-mail é obrigatório.")
            erro_validacao = True
            
        if not erro_validacao:
            sucesso_morador, msg_morador = editar_morador(
                cpf_morador, novo_nome, novo_email, novo_id_residencia, novo_sindico
            )
            
            sucesso_telefone = True
            if id_tel_db and novo_telefone != num_tel_db:
                sucesso_telefone = editar_telefone(id_tel_db, novo_telefone)

            if sucesso_morador and sucesso_telefone:
                st.success("Dados atualizados com sucesso!")
                time.sleep(1)
                st.session_state.morador_edit = None 
                st.switch_page("pages/listagemMoradorResidencia.py")
            else:
                st.error(f"Erro ao salvar: {msg_morador}")
                if not sucesso_telefone:
                    st.warning("Ocorreu um erro ao atualizar o telefone.")