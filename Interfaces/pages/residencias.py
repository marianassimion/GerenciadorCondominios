import streamlit as st
import time
from db_functions import listar_residencias, obter_condominio_por_cnpj, deletar_residencia, login_sessao

st.set_page_config(page_title="Residências", layout="centered")

login_sessao()

if 'detail_cnpj' not in st.session_state:
    st.warning("Selecione um condomínio primeiro.")
    st.stop()

cnpj = st.session_state.detail_cnpj

residencias = listar_residencias(cnpj)
dados_condominio = obter_condominio_por_cnpj(cnpj)

if dados_condominio:
    nome, log, bai, cid, uf, cep = dados_condominio
    st.title(f"🏢 {nome}")
    st.caption(f"{log}, {bai} - {cid}/{uf} | CEP: {cep}")
    st.caption(f"CNPJ: {cnpj}")


st.subheader("Unidades Cadastradas")
with st.container(height=500, border=True):
    if not residencias:
        st.info("Nenhuma residência cadastrada neste condomínio.")
            
    for residencia in residencias:
        id_res, numero, bloco, tipo = residencia
            
        with st.container(border=True):
            c_icon, c_info, c_ver, c_edit, c_del = st.columns([0.5, 4, 0.5, 0.5, 0.5], vertical_alignment="center")
            
            c_icon.image("./img/apt.png", width=70)
            
            c_info.write(f"**{tipo} {numero}** - {bloco}")
                
            
            if c_ver.button(":material/visibility:", key=f"ver_{id_res}", help="Detalhes"):
                st.session_state['detail_residencia'] = id_res                
                st.switch_page("pages/detalharResidencia.py")
            
            if c_edit.button(":material/edit_square:", key=f"edit_{id_res}", help="Editar residência"):
                st.session_state['residencia_edit'] = id_res                
                st.switch_page("pages/edicaoResidencia.py")

            if c_del.button(":material/delete:", key=f"del_{id_res}", help="Excluir residência"):
                if deletar_residencia(id_res):
                    st.success("Unidade removida!") 
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Erro ao excluir.")

if st.button("Cadastrar Nova Residência", type="primary", use_container_width=True):
    st.switch_page("pages/cadastroResidencia.py")

if st.button("Voltar para Condomínios", use_container_width=True):
        st.switch_page("pages/detalharCodominio.py") 