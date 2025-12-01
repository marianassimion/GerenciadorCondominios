import streamlit as st
import time
from db_controller import login_sessao, obter_condominio_por_cnpj, obter_empregados, deletar_empregado

st.set_page_config(page_title="Detalhes do Condomínio")


login_sessao()

if 'detail_cnpj' not in st.session_state or st.session_state.detail_cnpj is None:
    st.warning("Nenhum condomínio selecionado para edição.")
    if st.button("Voltar para Home"): 
        st.switch_page("pages/home.py")
    st.stop() # Para a execução

cnpj_atual = st.session_state.detail_cnpj

if st.button("Voltar para Home"):
    st.switch_page("pages/home.py")


dados_condominio = obter_condominio_por_cnpj(cnpj_atual)
empregados = obter_empregados(cnpj_atual)

if dados_condominio:
    nome, log, bai, cid, uf, cep = dados_condominio
    
    # Cabeçalho do Condomínio
    st.title(f"🏢 {nome}")
    st.caption(f"{log}, {bai} - {cid}/{uf} | CEP: {cep}")
    st.caption(f"CNPJ: {cnpj_atual}")
    st.divider()

    # --- SEÇÃO DE AVISOS ---
    col_tit, col_btn = st.columns([3, 1], vertical_alignment="bottom")
    if col_btn.button("Quadro de avisos", use_container_width=True):
        st.switch_page("pages/listagemAvisos.py")

    # --- SEÇÃO DE EMPREGADOS ---
    col_tit, col_btn = st.columns([3, 1], vertical_alignment="bottom")
    col_tit.subheader("Quadro de Funcionários")
    
    if col_btn.button("Novo Empregado", use_container_width=True):
        st.switch_page("pages/cadastroEmpregado.py")

    # Cabeçalho da Tabela
    c1, c2, c3, c4, c5, c_edit, c_del = st.columns([2.5, 2, 1.2, 1.5, 1.5, 0.8, 0.8], vertical_alignment="center")
    c1.markdown("**Nome**")
    c2.markdown("**Cargo**")
    c3.markdown("**Matrícula**")
    c4.markdown("**Admissão**")
    c5.markdown("**Salário**")
    st.markdown("<hr style='margin: 5px 0; border: none; border-top: 1px solid #333; opacity: 0.2;'>", unsafe_allow_html=True)

    if empregados:
        with st.container(height=400, border=False):
            for emp in empregados:
                # Recupera dados (incluindo CPF no índice 5)
                nome_e, cargo_e, mat_e, data_e, sal_e, cpf_e = emp

                c1, c2, c3, c4, c5, c_edit, c_del = st.columns([2.5, 2, 1.2, 1.5, 1.5, 0.8, 0.8], vertical_alignment="center")
                c1.write(nome_e)
                c2.write(cargo_e)
                c3.write(str(mat_e))
                c4.write(str(data_e))
                c5.write(f"R$ {sal_e}")
                
                with c_edit:
                    if st.button(":material/edit_square:", key=f"edit_emp_{cpf_e}", help="Editar funcionário"):
                        st.session_state.editing_cpf = cpf_e
                        st.switch_page("pages/edicaoEmpregado.py")

                with c_del:
                    if st.button(":material/delete:", key=f"del_emp_{cpf_e}", help="Excluir"):
                        if deletar_empregado(cpf_e):
                            st.success("Funcionário excluído!")
                            time.sleep(1)
                            st.rerun()
                st.write("---")
    else:
        st.info("Nenhum funcionário cadastrado neste condomínio.")

else:
    st.error("Erro ao carregar dados do condomínio.")