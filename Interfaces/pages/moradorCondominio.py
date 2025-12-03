import streamlit as st
import time
from db_functions import obter_condominio_por_cnpj, deletar_morador, login_sessao, listar_moradores_condominio

st.set_page_config(page_title="Moradores", layout="centered")

login_sessao()

# Verifica se há um condomínio selecionado na sessão
if 'detail_cnpj' not in st.session_state:
    st.warning("Selecione um condomínio primeiro.")
    st.stop()

cnpj = st.session_state.detail_cnpj

# Obtém dados do condomínio para o cabeçalho
dados_condominio = obter_condominio_por_cnpj(cnpj)

if dados_condominio:
    nome, log, bai, cid, uf, cep = dados_condominio
    st.title(f"🏢 {nome}")
    st.caption(f"{log}, {bai} - {cid}/{uf} | CEP: {cep}")
    st.caption(f"CNPJ: {cnpj}")

st.subheader("Moradores do Condomínio")

# Busca os moradores no banco
moradores = listar_moradores_condominio(cnpj)

with st.container(height=500, border=True):

    if not moradores:
        st.info("Nenhum morador cadastrado neste condomínio.")
    
    for morador in moradores:
        cpf, nome, email, sindico, id_residencia, num_unidade, bloco, tipo = morador

        with st.container(border=True):
            
            # Ajustei as colunas para caber melhor as informações
            c_icon, c_info, c_det, c_veic, c_tel, c_edit, c_del = st.columns(
                [0.7, 4, 0.7, 0.7, 0.7, 0.7, 0.7],
                vertical_alignment="center"
            )

            # Ícone
            # Certifique-se que a imagem existe ou use um ícone do st
            try:
                c_icon.image("./img/morador.png", width=60)
            except:
                c_icon.write("👤") 

            sind_text = "- Síndico" if sindico else ""
            c_info.write(f"{nome} {sind_text}")
            c_info.write(f"🏠 {tipo} {num_unidade} - {bloco}")
            c_info.caption(f"CPF: {cpf} | {email}")

            # Botões de Ação
            if c_det.button(":material/visibility:", key=f"det_{cpf}", help="Detalhes"):
                st.session_state['detail_morador'] = cpf
                st.switch_page("pages/detalhesMorador.py")

            if c_veic.button(":material/directions_car:", key=f"veic_{cpf}", help="Veículos"):
                st.session_state['veiculo_morador'] = cpf
                st.switch_page("pages/veiculos.py")
            
            if c_edit.button(":material/edit_square:", key=f"edit_{cpf}", help="Editar Morador"):
                st.session_state['morador_edit'] = cpf
                st.switch_page("pages/edicaoMorador.py")

            if c_tel.button(":material/phone_enabled:", key=f"tel_{cpf}", help="Cadastrar novo telefone"):
                st.session_state['morador_phone'] = cpf
                st.switch_page("pages/cadastroTelefone.py")

            if c_del.button(":material/delete:", key=f"del_{cpf}", help="Excluir Morador"):
                if deletar_morador(cpf):
                    st.success("Morador removido!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Erro ao excluir morador.")

col_voltar, col_novo = st.columns(2)

with col_novo:
    if st.button("Cadastrar Novo Morador", type="primary", use_container_width=True):
        st.switch_page("pages/cadastroMorador.py")

with col_voltar:
    if st.button("Voltar para Residências", use_container_width=True):
        st.switch_page("pages/home.py") 
       