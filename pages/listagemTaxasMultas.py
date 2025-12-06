import streamlit as st
import time
from src.db_functions import obter_residencia_por_id, listar_taxas_residencia, listar_multas_residencia, deletar_taxa, deletar_multa, login_sessao

st.set_page_config(page_title="Taxas e Multas", layout="centered")

login_sessao()

if "detail_residencia" not in st.session_state:
    st.warning("Nenhuma residência selecionada.")
    st.stop()

id_residencia = st.session_state.detail_residencia
dados_residencia = obter_residencia_por_id(id_residencia)

if not dados_residencia:
    st.error("Residência não encontrada.")
    st.stop()

id_res, num_unidade, bloco, tipo, cnpj_cond = dados_residencia

st.title("💰 Taxas & Multas")
st.caption(f"📍 {tipo} {num_unidade} - {bloco} | Condominio CNPJ: {cnpj_cond}")

tab_taxas, tab_multas = st.tabs(["💵 Taxas", "⚠️ Multas"])

# TAXAS
with tab_taxas:
    col_header, col_btn = st.columns([3, 1.5], vertical_alignment="bottom")
    col_header.subheader("Taxas da Residência")

    if col_btn.button("Nova Taxa", type="primary", use_container_width=True):
        st.switch_page("pages/cadastroTaxa.py")

    taxas = listar_taxas_residencia(id_residencia)

    with st.container(height=500, border=True):
        if not taxas:
            st.info("Nenhuma taxa cadastrada para esta residência.")

        for taxa in taxas:
            id_taxa, data_emissao, data_vencimento, valor, status, id_residencia = taxa

            if status == "Pago":
                cor_status = "green"
                icone_status = "✅"
            elif status == "Pendente":
                cor_status = "orange"
                icone_status = "⏳"
            else:
                cor_status = "red"
                icone_status = "⛔"

            with st.container(border=True):
                c_icon, c_details, c_status, c_actions = st.columns([0.5, 3, 1.5, 1])

                with c_icon:
                    st.markdown("💵") 

                with c_details:
                    st.markdown(f"**Vencimento: {data_vencimento}**")
                    st.caption(f"Emissão: {data_emissao}")

                with c_status:
                    st.markdown(f"### {valor}")
                    st.markdown(f":{cor_status}[{icone_status} {status}]")

                with c_actions:
                    if st.button(":material/edit_square:", key=f"edit_taxa_{id_taxa}", help="Editar Taxa"):
                        st.session_state["taxa_edit"] = id_taxa
                        st.switch_page("pages/edicaoTaxa.py")

                    if st.button(":material/delete:", key=f"del_taxa_{id_taxa}", help="Excluir Taxa", type="secondary"):
                        if deletar_taxa(id_taxa):
                            st.toast("Taxa excluída com sucesso!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Erro ao excluir.")

# MULTAS
with tab_multas:
    col_header, col_btn = st.columns([3, 1.5], vertical_alignment="bottom")
    col_header.subheader("Multas da Residência")

    if col_btn.button("Nova Multa", type="primary", use_container_width=True):
        st.switch_page("pages/cadastroMulta.py")

    multas = listar_multas_residencia(id_residencia)
    with st.container(height=500, border=True):
        if not multas:
            st.info("Nenhuma multa cadastrada para esta residência.")

        for multa in multas:
            id_multa, data_emissao, data_vencimento, status, valor, descricao, id_residencia = multa

            if status == "Pago":
                cor_status = "green"
                icone_status = "✅"
            elif status == "Pendente":
                cor_status = "orange"
                icone_status = "⏳"
            else:
                cor_status = "red"
                icone_status = "⛔"

            with st.container(border=True):
                c_icon, c_details, c_status, c_actions = st.columns([0.5, 3, 1.5, 1])

                with c_icon:
                    st.markdown("🗒️") 

                with c_details:
                    st.markdown(f"**Vencimento: {data_vencimento}**")
                    st.caption(f"Emissão: {data_emissao}")

                with c_status:
                    st.markdown(f"### {valor}")
                    st.markdown(f":{cor_status}[{icone_status} {status}]")

                with c_actions:
                    if st.button(":material/edit_square:", key=f"edit_multa_{id_multa}", help="Editar Multa"):
                        st.session_state["multa_edit"] = id_multa
                        st.switch_page("pages/edicaoMulta.py")

                    if st.button(":material/delete:",key=f"del_multa_{id_multa}",help="Excluir Multa",type="secondary"):
                        if deletar_multa(id_multa):
                            st.toast("Multa excluída com sucesso!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Erro ao excluir.")

if st.button("Voltar para Residências", use_container_width=True):
    st.switch_page("pages/listagemResidencias.py")