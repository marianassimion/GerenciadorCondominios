import streamlit as st
import time
from db_functions import obter_empregado_por_cpf, atualizar_empregado

st.set_page_config(page_title="Editar Empregado")

if 'editing_cpf' not in st.session_state or st.session_state.editing_cpf is None:
    st.warning("Nenhum empregado selecionado para edição.")
    if st.button("Voltar para Home"):
        st.switch_page("pages/home.py")
    st.stop()

cpf_atual = st.session_state.editing_cpf

if st.button("Cancelar e Voltar"):
    st.session_state.details_condominio_mode = True # Garante que volta para os detalhes
    st.switch_page("pages/listagemEmpregados.py")

st.title("Editar Empregado")

dados = obter_empregado_por_cpf(cpf_atual)

if dados:
    nome_at, cargo_at, mat_at, data_at, sal_at, cpf_at, foto_at = dados

    with st.form("form_editar_empregado"):
        st.caption(f"Editando funcionário (CPF: {cpf_atual})")
        
        nome = st.text_input("Nome Completo", value=nome_at)
        
        c1, c2 = st.columns(2)
        # CPF Bloqueado 
        c1.text_input("CPF", value=cpf_at, disabled=True) 
        cargo = c2.text_input("Cargo", value=cargo_at)
        
        c3, c4, c5 = st.columns(3)
        matricula = c3.text_input("Matrícula", value=str(mat_at))
        data_adm = c4.date_input("Data de Admissão", value=data_at)
        salario = c5.number_input("Salário", value=float(sal_at), step=100.0)
        st.write("Foto atual:")
        if foto_at:
            st.image(foto_at, width=200)
        else:
            st.info("Este funcionário não possui foto cadastrada.")

        foto = st.file_uploader("Foto do funcionário", type=["jpg", "jpeg", "png"])
        foto_bytes = foto.read() if foto else None

        salvar = st.form_submit_button("Salvar Alterações", type="primary", use_container_width=True)

    # --- LÓGICA DE SALVAR ---
    if salvar:
        if not nome:
            st.error("O nome é obrigatório.")
        else:
            sucesso = atualizar_empregado(nome, cargo, matricula, data_adm, salario, foto_bytes, cpf_atual )
            
            if sucesso:
                st.success("Dados atualizados com sucesso!")
                time.sleep(1)
                
                st.session_state.details_condominio_mode = True 
                st.switch_page("pages/listagemEmpregados.py")
else:
    st.error("Empregado não encontrado.")