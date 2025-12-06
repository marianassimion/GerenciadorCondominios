import streamlit as st
import time
from src.db_functions import obter_residencia_por_id, editar_residencia

st.set_page_config(page_title="Editar Residência", layout="centered")


if 'residencia_edit' not in st.session_state:
    st.error("Nenhuma residência selecionada.")
    time.sleep(2)
    st.switch_page("pages/listagemResidencias.py")

id_residencia = st.session_state.residencia_edit

st.title("Editar Residência")


dados_residencia = obter_residencia_por_id(id_residencia)

if dados_residencia:
    id_residencia, num, bloco, tipo, cnpj = dados_residencia

    with st.form("form_editar_residencia"):
        st.caption(f"Editando Residência ID: {id_residencia}")

        col_info1, col_info2 = st.columns(2)
        
        with col_info1:
            st.text_input("ID do Sistema", value=id_residencia, disabled=True)
            
        with col_info2:
            st.text_input(
                "Condomínio", 
                value=cnpj, 
                disabled=True, 
                help="Este campo não pode ser alterado."
            )

        st.divider()
        
        st.subheader("Dados da Unidade")
        
        c1, c2, c3 = st.columns([1, 1, 2])
        
        with c1:
            novo_num = st.text_input("Número", value=num)
        
        with c2:
            novo_bloco = st.text_input("Bloco", value=bloco)

        with c3:
            tipos_comuns = ["Apartamento", "Casa", "Cobertura", "Studio"]
            if tipo not in tipos_comuns:
                tipos_comuns.append(tipo)
            novo_tipo = st.selectbox(
                "Tipo", 
                options=tipos_comuns, 
                index=tipos_comuns.index(tipo)
            )

        st.markdown("<br>", unsafe_allow_html=True)

        salvar = st.form_submit_button(
            "Salvar Alterações", 
            type="primary", 
            use_container_width=True
        )

    if st.button("Cancelar", use_container_width=True):
        del st.session_state["residencia_edit"]
        st.switch_page("pages/listagemResidencias.py")

    if salvar:
        if not novo_num or not novo_bloco:
            st.error("Número e Bloco são obrigatórios.")
        else:
            sucesso = editar_residencia(
                id_residencia, 
                novo_num, 
                novo_bloco, 
                novo_tipo
            )
            
            if sucesso:
                st.success("Residência atualizada com sucesso!")
                time.sleep(1)
                del st.session_state["residencia_edit"]
                st.switch_page("pages/listagemResidencias.py")

else:
    st.error("Erro ao carregar os dados da residência.")
