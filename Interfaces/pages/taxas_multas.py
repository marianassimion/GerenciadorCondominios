import streamlit as st
import time
from db_functions import obter_residencia_por_id, listar_taxas_residencia, listar_multas_residencia, deletar_taxa, deletar_multa, login_sessao

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

st.title(f"💰 Taxas & Multas")
st.caption(f"{tipo} {num_unidade} - {bloco}")
st.caption(f"CNPJ do Condomínio: {cnpj_cond}")

tab_taxas, tab_multas = st.tabs(["💵 Taxas", "⚠️ Multas"])

with tab_taxas:

    st.subheader("Taxas da Residência")

    taxas = listar_taxas_residencia(id_residencia)

    with st.container(height=500, border=True):

        if not taxas:
            st.info("Nenhuma taxa cadastrada para esta residência.")

        for taxa in taxas:
            id_taxa, data_emissao, data_vencimento, valor, status = lis

            with st.container(border=True):
                c_icon, c_info, c_edit, c_del = st.columns(
                    [0.8, 4, 0.8, 0.8],
                    vertical_alignment="center"
                )

                c_icon.image("./img/tax.png", width=60)

                c_info.write(f"**Valor: R$ {valor:.2f}** — {status}")
                c_info.caption(f"Emissão: {data_emissao}")
                c_info.caption(f"Vencimento: {data_venc}")

                if c_edit.button(":material/edit_square:", key=f"edit_taxa_{id_taxa}", help="Editar Taxa"):
                    st.session_state["taxa_edit"] = id_taxa
                    st.switch_page("pages/edicaoTaxa.py")

                if c_del.button(":material/delete:", key=f"del_taxa_{id_taxa}", help="Excluir Taxa"):
                    if deletar_taxa(id_taxa):
                        st.success("Taxa excluída!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Erro ao excluir taxa.")

    if st.button("Cadastrar Nova Taxa", type="primary", use_container_width=True):
        st.switch_page("pages/cadastroTaxa.py")


with tab_multas:

    st.subheader("Multas da Residência")

    multas = listar_multas_residencia(id_residencia)

    with st.container(height=500, border=True):

        if not multas:
            st.info("Nenhuma multa cadastrada para esta residência.")

        for multa in multas:
            id_multa = multa["id_multa"]
            motivo = multa["motivo"]
            data = multa["data"]
            valor = multa["valor"]

            with st.container(border=True):
                c_icon, c_info, c_edit, c_del = st.columns(
                    [0.8, 4, 0.8, 0.8],
                    vertical_alignment="center"
                )

                c_icon.image("./img/warning.png", width=60)

                c_info.write(f"**R$ {valor:.2f}** — {motivo}")
                c_info.caption(f"Data: {data}")

                if c_edit.button(":material/edit_square:", key=f"edit_multa_{id_multa}", help="Editar Multa"):
                    st.session_state["multa_edit"] = id_multa
                    st.switch_page("pages/edicaoMulta.py")

                if c_del.button(":material/delete:", key=f"del_multa_{id_multa}", help="Excluir Multa"):
                    if deletar_multa(id_multa):
                        st.success("Multa excluída!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Erro ao excluir multa.")

    if st.button("Cadastrar Nova Multa", type="primary", use_container_width=True):
        st.switch_page("pages/cadastroMulta.py")

if st.button("Voltar para Residências", use_container_width=True):
    st.switch_page("pages/residencias.py")
