import streamlit as st
import time
from db_functions import obter_condominio_por_cnpj, obter_empregados, listar_avisos, deletar_aviso

st.set_page_config(page_title="Listagem de Avisos")

if 'detail_cnpj' not in st.session_state or st.session_state.detail_cnpj is None:
    st.warning("Nenhum condomínio selecionado para listagem.")
    if st.button("Voltar para Home"): 
        st.switch_page("pages/detalharCondominio.py")
    st.stop() # Para a execução

# Pegamos o CNPJ da memória
cnpj_atual = st.session_state.detail_cnpj

dados_condominio = obter_condominio_por_cnpj(cnpj_atual)
empregados = obter_empregados(cnpj_atual)

if st.button("Voltar para Condomínio"):
    st.switch_page("pages/detalharCondominio.py")


col_tit, col_btn = st.columns([3, 1], vertical_alignment="bottom")
col_tit.subheader("Quadro de Avisos")

if col_btn.button("Novo Aviso", use_container_width=True):
        # Redireciona para a página de cadastro de empregado
        st.switch_page("pages/cadastroAviso.py")

avisos = listar_avisos(cnpj_atual)

if avisos:
    with st.container(height=500, border=False):
        
        for aviso in avisos:
            id_a, titulo, texto, data, autor, cnpj_condominio = aviso
            
            # Formata a data
            data_formatada = data.strftime("%d/%m/%Y às %H:%M")

            # --- O CARD DO AVISO ---
            with st.container(border=True):
                col_content, col_action = st.columns([0.9, 0.1])
                
                with col_content:
                    st.markdown(f"**{autor}** <span style='color:grey; font-size:0.8em;'> • {data_formatada}</span>", unsafe_allow_html=True)
                    
                    st.markdown(f"#### {titulo}")
                    
                    st.write(texto)

                with col_action:
                    # Botão de Excluir (Lixeira) no canto direito
                    if st.button(":material/delete:", key=f"del_aviso_{id_a}", help="Excluir este aviso"):
                        if deletar_aviso(id_a):
                            st.toast("Aviso removido!")
                            time.sleep(1)
                            st.rerun()
else:
    st.info("Nenhum aviso publicado ainda.")