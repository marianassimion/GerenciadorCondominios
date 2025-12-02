import streamlit as st
import time
from db_functions import obter_condominio_por_cnpj, listar_areas_comuns, deletar_area_comum, criar_area_comum, obter_area_comum

st.set_page_config(page_title="Listagem de Áreas comuns")

if 'detail_cnpj' not in st.session_state or st.session_state.detail_cnpj is None:
    st.warning("Nenhum condomínio selecionado para listagem.")
    if st.button("Voltar para Home"): 
        st.switch_page("pages/detalharCondominio.py")
    st.stop() 

# Pega o CNPJ da memória
cnpj_atual = st.session_state.detail_cnpj

if st.button("Voltar para Condomínio"):
    st.switch_page("pages/detalharCondominio.py")

dados_condominio = obter_condominio_por_cnpj(cnpj_atual)
areas_comuns = listar_areas_comuns(cnpj_atual)
nome_condominio = dados_condominio[0] if dados_condominio else "Não identificado"

col_tit, col_btn = st.columns([3, 1], vertical_alignment="bottom")
col_tit.subheader("Listagem de áreas comuns")
st.write(f"{nome_condominio}")

if col_btn.button("Nova área comum", use_container_width=True):
        st.switch_page("pages/cadastroAreaComum.py")

if areas_comuns:
    with st.container(height=500, border=False):
        
        for area in areas_comuns:
            id_a, nome_a, desc_a, cap_a = area
            
            # --- O CARD DE ÁREA---
            with st.container(border=True):
                c_content, c_edit, c_del = st.columns([0.8, 0.1, 0.1])
                
                with c_content:
                    st.markdown(f"#### {nome_a} ", unsafe_allow_html=True)
                    st.markdown(f"{desc_a}")
                    st.write(f"Capacidade: {cap_a} pessoas")

                with c_del:
                    if st.button(":material/delete:", key=f"del_area_comum_{id_a}", help="Excluir essa área comum"):
                        if deletar_area_comum(id_a):
                            st.toast("Área comum excluída!")
                            time.sleep(2)
                            st.rerun()

                with c_edit:
                    if st.button(":material/edit_square:", key=f"edit_area_comum_{id_a}", help="Editar essa área comum"):
                        st.session_state.editing_area_comum = id_a
                        st.switch_page("pages/edicaoAreaComum.py")

else:
    st.info("Nenhuma área comum cadastrada neste condomínio.")