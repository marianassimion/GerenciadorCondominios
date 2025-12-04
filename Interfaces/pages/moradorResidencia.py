import streamlit as st
import time
from db_functions import obter_residencia_por_id,listar_moradores_residencia, listar_moradores_residencia, deletar_morador, login_sessao

st.set_page_config(page_title="Moradores", layout="centered")

login_sessao()

if 'detail_residencia' not in st.session_state:
    st.warning("Nenhuma residência selecionada.")
    st.stop()

id_residencia = st.session_state.detail_residencia

dados_residencia = obter_residencia_por_id(id_residencia)

if dados_residencia:
    id, num_unidade, bloco, tipo, cnpj_cond = dados_residencia

st.title(f"🏠 {tipo} {num_unidade} - {bloco}")
st.caption(f"CNPJ do Condomínio: {cnpj_cond}")

st.subheader("Moradores da Unidade")

moradores = listar_moradores_residencia(id_residencia)

with st.container(height=500, border=True):

    if not moradores:
        st.info("Nenhum morador cadastrado nesta residência.")
    
    for morador in moradores:
        cpf, nome, email, sindico = morador

        with st.container(border=True):

            c_icon, c_info, c_veic, c_tel, c_edit, c_del = st.columns(
                [0.7, 4, 0.7, 0.7, 0.7, 0.7],
                vertical_alignment="center"
            )

            c_icon.image("./img/morador.png", width=70)
            sind_text = " (Síndico)" if sindico else ""
            c_info.write(f"**{nome}{sind_text}**")
            c_info.caption(f"CPF: {cpf}")
            c_info.caption(email)

            if c_veic.button(":material/directions_car:", key=f"veic_{cpf}", help="Veículos"):
                st.session_state['veiculo_morador'] = cpf
                st.switch_page("pages/veiculos.py")

            if c_edit.button(":material/edit_square:", key=f"edit_{cpf}", help="Editar Morador"):
                st.session_state['morador_edit'] = cpf
                st.switch_page("pages/edicaoMorador.py")

            if c_tel.button(":material/phone_enabled:", key=f"tel_{cpf}", help="Telefones"):
                st.session_state['morador_phone'] = cpf
                st.switch_page("pages/listagemTelefones.py")

            if c_del.button(":material/delete:", key=f"del_{cpf}", help="Excluir Morador"):
                if deletar_morador(cpf):
                    st.success("Morador removido!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Erro ao excluir morador.")


if st.button("Cadastrar Novo Morador", type="primary", use_container_width=True):
    st.switch_page("pages/cadastroMorador.py")

if st.button("Voltar para Residências", use_container_width=True):
    st.switch_page("pages/residencias.py")
