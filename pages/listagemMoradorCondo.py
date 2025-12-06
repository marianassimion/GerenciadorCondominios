import streamlit as st
import time
from src.db_functions import obter_condominio_por_cnpj, deletar_morador, login_sessao, listar_moradores_condominio

st.set_page_config(page_title="Moradores", layout="centered")

login_sessao()

if 'detail_cnpj' not in st.session_state:
    st.warning("Selecione um condomínio primeiro.")
    st.stop()

cnpj = st.session_state.detail_cnpj

dados_condominio = obter_condominio_por_cnpj(cnpj)

if dados_condominio:
    nome, log, bai, cid, uf, cep = dados_condominio
    st.title(f"🏢 {nome}")
    st.caption(f"{log}, {bai} - {cid}/{uf} | CEP: {cep}")
    st.caption(f"CNPJ: {cnpj}")

st.subheader("Moradores do Condomínio")

moradores = listar_moradores_condominio(cnpj)

with st.container(height=500, border=True):
    if not moradores:
        st.info("Nenhum morador cadastrado nesse condomínio.")
    
    for morador in moradores:
        cpf, nome, email, sindico, id_residencia, num_unidade, bloco, tipo = morador

        with st.container(border=True):
            
            c_icon, c_info, c_det, c_del = st.columns([0.7, 4, 0.7, 0.7],vertical_alignment="center")

            try:
                c_icon.image("./src/Interface/img/morador.png", width=70)
            except:
                c_icon.write("👤") 

            sind_text = "- Síndico" if sindico else ""
            c_info.write(f"{nome} {sind_text}")
            c_info.write(f"🏠 {tipo} {num_unidade} - {bloco}")
            c_info.caption(f"CPF: {cpf} | {email}")

            if c_det.button(":material/visibility:", key=f"det_{cpf}", help="Detalhes"):
                st.session_state['detail_morador'] = cpf
                st.session_state['detail_residencia'] = id_residencia
                st.switch_page("pages/detalhesMorador.py")

            if c_del.button(":material/delete:", key=f"del_{cpf}", help="Excluir Morador"):
                if deletar_morador(cpf):
                    st.success("Morador removido!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Erro ao excluir morador.")


if st.button("Voltar para Condomínios", use_container_width=True):
    st.switch_page("pages/home.py") 
       