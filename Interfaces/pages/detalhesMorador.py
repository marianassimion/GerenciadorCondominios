import streamlit as st
import time
from db_functions import obter_residencia_por_id, obter_morador_por_id, login_sessao, listar_telefones_morador, deletar_telefone

st.set_page_config(page_title="Detalhes do Morador", layout="centered")

login_sessao()

if 'detail_residencia' not in st.session_state:
    st.warning("Nenhuma residência selecionada.")
    time.sleep(1)
    st.switch_page("pages/residencias.py") 

id_residencia = st.session_state.detail_residencia

if 'detail_morador' not in st.session_state: 
     st.warning("Nenhum morador selecionado.")
     st.stop()

morador_cpf = st.session_state.detail_morador

dados_residencia = obter_residencia_por_id(id_residencia)
dados_morador = obter_morador_por_id(morador_cpf)
telefones = listar_telefones_morador(morador_cpf)

if dados_residencia:
    id_res, num_unidade, bloco, tipo, cnpj_cond = dados_residencia

if dados_morador:
    cpf, nome, email, id_res_fk, sindico = dados_morador

st.title(f"👤 {nome}")
st.markdown(f"**CPF:** `{cpf}` | **Email:** {email}")
st.info(f"🏠 **{tipo} {num_unidade}** - Bloco {bloco}")
st.divider()

st.subheader("📞 Telefones de Contato")

with st.container(border=True):
    
    if not telefones:
        st.warning("Nenhum telefone cadastrado para este morador.")
    
    for item in telefones:
        id_tel, numero_tel = item 

        with st.container():
            c_icon, c_tel, c_edit, c_del = st.columns([0.4, 3, 0.5, 0.5], vertical_alignment="center")

            with c_icon:
                st.markdown(":material/phone:") 

            with c_tel:
                st.markdown(f"**{numero_tel}**")

            with c_edit:
                if st.button(":material/edit_square:", key=f"edit_{id_tel}", help="Editar telefone"):
                    st.session_state['telefone_editar_id'] = id_tel
                    st.session_state['telefone_editar_numero'] = numero_tel
                    st.session_state['morador_phone'] = cpf 
                    st.switch_page("pages/cadastroTelefone.py")

            with c_del:
                if st.button(":material/delte:", key=f"del_{id_tel}", type="primary", help="Excluir telefone"):
                    if deletar_telefone(id_tel):
                        st.toast("Telefone excluído com sucesso!")
                        time.sleep(1.5) 
                        st.rerun() 
                    else:
                        st.error("Erro ao deletar o telefone. Tente novamente.")
            

with st.container():
    if st.button("Voltar para Moradores", use_container_width=True):
        st.switch_page("pages/moradorResidencia.py")