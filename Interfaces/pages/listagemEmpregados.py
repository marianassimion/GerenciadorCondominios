import streamlit as st
import time
from db_functions import obter_condominio_por_cnpj, obter_empregados, deletar_empregado, obter_media_salarial_por_condominio

st.set_page_config(page_title="Listagem de Empregados")

if 'detail_cnpj' not in st.session_state or st.session_state.detail_cnpj is None:
    st.warning("Nenhum condomínio selecionado para listagem.")
    if st.button("Voltar para Home"): 
        st.switch_page("pages/detalharCondominio.py")
    st.stop() # Para a execução

# Pegamos o CNPJ da memória
cnpj_atual = st.session_state.detail_cnpj

if st.button("Voltar para Condomínio"):
    st.switch_page("pages/detalharCondominio.py")

dados_condominio = obter_condominio_por_cnpj(cnpj_atual)
empregados = obter_empregados(cnpj_atual)
id_condominio = dados_condominio[0]
media_salarial = obter_media_salarial_por_condominio(cnpj_atual)

col_tit, col_btn = st.columns([3, 1], vertical_alignment="bottom")
col_tit.subheader("Quadro de Funcionários")

if col_btn.button("Novo Empregado", use_container_width=True):
        # Redireciona para a página de cadastro de empregado
        st.switch_page("pages/cadastroEmpregado.py")

c1, c2, c3, c4, c5,c6, c_edit, c_del = st.columns([2, 1.5, 1.2, 1.5, 1, 1, 0.8, 0.8], vertical_alignment="center")
c1.markdown("**Nome**")    
c2.markdown("**Cargo**")
c3.markdown("**Matrícula**")
c4.markdown("**Admissão**")
c5.markdown("**Salário**")
c6.markdown("**Foto**")

st.markdown("<hr style='margin: 5px 0; border: none; border-top: 1px solid #333; opacity: 0.2;'>", unsafe_allow_html=True)

if empregados:
    with st.container(height=450, border=False):
        for emp in empregados:
            # Recupera dados (incluindo CPF no índice 5)
            nome_e, cargo_e, mat_e, data_e, sal_e, cpf_e, foto_e = emp

            c1, c2, c3, c4, c5, c6, c_edit, c_del = st.columns([2, 1.5, 1.2, 1.5, 1, 1, 0.8, 0.8], vertical_alignment="center")
            c1.write(nome_e)
            c2.write(cargo_e)
            c3.write(str(mat_e))
            c4.write(str(data_e))
            c5.write(f"R$ {sal_e}")
            if foto_e:
                c6.image(foto_e, width=60)

            else: 
                c6.image("https://cdn-icons-png.flaticon.com/512/149/149071.png", width=60)


            with c_edit:
                if st.button(":material/edit_square:", key=f"edit_emp_{cpf_e}", help="Editar funcionário"):                        
                    st.session_state.editing_cpf = cpf_e
                    st.switch_page("pages/edicaoEmpregado.py")

            with c_del:
                if st.button(":material/delete:", key=f"del_emp_{cpf_e}", help="Excluir"):
                    if deletar_empregado(cpf_e):
                        st.success("Funcionário excluído!") #corrgir tamanho
                        time.sleep(1)
                        st.rerun()
            st.write("---")

else:
    st.info("Nenhum funcionário cadastrado neste condomínio.")

st.metric(label="Média Salarial do Condomínio", value=f"R$ {media_salarial:,.2f}")