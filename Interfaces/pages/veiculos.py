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

if 'detail_residencia' not in st.session_state:
    st.warning("Nenhuma residência selecionada.")
    time.sleep(1)
    st.switch_page("pages/residencias.py") 

id_residencia = st.session_state.detail_residencia

if 'veiculo_morador' not in st.session_state: 
     st.warning("Nenhum morador selecionado.")
     st.stop()

morador_cpf = st.session_state.veiculo_morador

dados_morador = obter_morador_por_id(morador_cpf)

cpf, nome, email, id_residencia, sindico = dados_morador

st.title(f"🚗 Veículos")
st.subheader(f"Morador: {nome}")
sindico_text = "Síndico" if sindico else ""
st.caption(f"CPF: {cpf} - {sindico_text}")
st.caption(email)

st.subheader("Veículos Cadastrados")

veiculos = listar_veiculos_morador(morador_cpf)

with st.container(height=500, border=True):

    if not veiculos:
        st.info("Nenhum veículo cadastrado para este morador.")

    for veic in veiculos:
        placa, modelo, cor = veic

        with st.container(border=True):

            c_icon, c_info, c_edit, c_del = st.columns(
                [0.8, 4, 0.7, 0.7],
                vertical_alignment="center"
            )

            # Ícone
            c_icon.image("./img/car.png", width=50)

            c_info.write(f"**{modelo}**")
            c_info.caption(f"Placa: {placa}")
            c_info.caption(f"Cor: {cor}")

            if c_edit.button(":material/edit_square:", key=f"edit_{placa}", help="Editar Veículo"):
                st.session_state["veiculo_edit_placa"] = placa
                st.switch_page("pages/edicaoVeiculo.py")

            if c_del.button(":material/delete:", key=f"del_{placa}", help="Excluir Veículo"):
                if deletar_veiculo(placa):
                    st.success("Veículo removido!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Erro ao excluir veículo.")


if st.button("Cadastrar Novo Veículo", type="primary", use_container_width=True):

    st.switch_page("pages/cadastroVeiculo.py")

if st.button("Voltar para Moradores", use_container_width=True):
    st.switch_page("pages/moradorResidencia.py")
