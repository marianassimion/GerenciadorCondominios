import streamlit as st
import time
from db_functions import (
    obter_morador_por_id,
    listar_veiculos_morador,
    deletar_veiculo,
    login_sessao
)

st.set_page_config(page_title="Veículos", layout="centered")

login_sessao()

if "veiculo_morador" not in st.session_state:
    st.warning("Nenhum morador selecionado.")
    st.stop()

cpf_morador = st.session_state.veiculo_morador

dados_morador = obter_morador_por_id(cpf_morador)

if not dados_morador:
    st.error("Morador não encontrado.")
    st.stop()

cpf, nome, email, id_residencia, sindico = dados_morador

st.title(f"🚗 Veículos")
st.subheader(f"**{nome}**")
st.caption(f"CPF: {cpf}")
st.caption(email)

st.subheader("Veículos Cadastrados")

veiculos = listar_veiculos_morador(cpf_morador)

with st.container(height=500, border=True):

    if not veiculos:
        st.info("Nenhum veículo cadastrado para este morador.")

    for veic in veiculos:
        placa, modelo, cor = veic

        with st.container(border=True):

            c_icon, c_info, c_edit, c_del = st.columns(
                [0.8, 4, 0.8, 0.8],
                vertical_alignment="center"
            )

            c_icon.markdown("🚗")

            c_info.write(f"**{modelo}**")
            c_info.caption(f"Placa: {placa}")
            c_info.caption(f"Cor: {cor}")


            if c_edit.button(":material/edit_square:", key=f"edit_{placa}", help="Editar Veículo"):
                st.session_state["veiculo_edit_placa"] = placa
                st.switch_page("pages/edicaoVeiculo.py")

            if c_del.button(":material/delete:", key=f"del_{placa}", help="Excluir Veículo"):
                if deletar_veiculo(placa):
                    st.success("Veículo excluído!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Erro ao excluir veículo.")


if st.button("Cadastrar Novo Veículo", type="primary", use_container_width=True):
    st.switch_page("pages/cadastroVeiculo.py")

if st.button("Voltar para Moradores", use_container_width=True):
    st.switch_page("pages/moradorResidencia.py")
