import streamlit as st
import time
from db_functions import obter_veiculos_por_condominio, buscar_veiculos_filtrados

st.set_page_config(page_title="Listagem de Veículos")

if 'detail_cnpj' not in st.session_state or st.session_state.detail_cnpj is None:
    st.warning("Nenhum condomínio selecionado.")
    if st.button("Voltar para Condomínios"): 
        st.switch_page("pages/home.py")
    st.stop() 

cnpj_atual = st.session_state.detail_cnpj

if st.button("Voltar para Condomínios"):
    st.switch_page("pages/home.py")

st.subheader("Controle de Veículos")

st.write("---") 


with st.container(border=True):
    c_busca, c_filtro, c_limpar = st.columns([3, 1.5, 0.5], vertical_alignment="bottom")
    
    termo_busca = c_busca.text_input("Pesquisar", placeholder="Digite para buscar...", label_visibility="collapsed")
    
    filtro_selecionado = c_filtro.selectbox(
        "Filtrar por:",
        ["Placa", "Morador", "Modelo"],
        label_visibility="collapsed"
    )
    
    if termo_busca:
        veiculos = buscar_veiculos_filtrados(cnpj_atual, termo_busca, filtro_selecionado)
        if c_limpar.button("❌", help="Limpar busca"):
            st.rerun() 
    else:
        veiculos = obter_veiculos_por_condominio(cnpj_atual)

st.caption(f"Exibindo {len(veiculos)} registros.")

c1, c2, c3, c4, c5 = st.columns([1.2, 2.5, 2, 1, 1.2], vertical_alignment="center")

c1.markdown("**Unidade**")    
c2.markdown("**Proprietário**")
c3.markdown("**Modelo**")
c4.markdown("**Cor**")
c5.markdown("**Placa**")

st.markdown("<hr style='margin: 5px 0; border: none; border-top: 1px solid #333; opacity: 0.2;'>", unsafe_allow_html=True)

if veiculos:
    with st.container(height=450, border=False):
        for vec in veiculos:
            unidade, morador, cpf_morador, modelo, cor, placa = vec

            c1, c2, c3, c4, c5 = st.columns([1.2, 2.5, 2, 1, 1.2], vertical_alignment="center")
            
            c1.write(unidade)
            c2.write(morador)
            c3.write(modelo)
            c4.write(cor)
            c5.write(placa)

            st.write("---")

else:
    if termo_busca:
        st.warning(f"Nenhum veículo encontrado com {filtro_selecionado}: '{termo_busca}'")
    else:
        st.info("Nenhum veículo cadastrado neste condomínio.")