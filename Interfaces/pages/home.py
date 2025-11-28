import streamlit as st
import mysql.connector
# Assumindo que config.py está no mesmo nível de diretório ou no path
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME 


# =========================================================================
# 1. CONEXÃO COM O BANCO DE DADOS
# =========================================================================

try:
    conexao = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conexao.cursor()
    print('Conexão bem-sucedida')

except mysql.connector.Error as err:
    st.error(f"Erro ao conectar no MySQL: Verifique as configurações no config.py. Erro: {err}")
    # Usar st.stop() para interromper a execução do Streamlit
    st.stop()


# =========================================================================
# 2. VARIÁVEIS E FUNÇÕES DE GESTÃO DE DADOS
# =========================================================================

admin_name = "Nome do Administrador"
admin_email = "admin@exemplo.com"

def listar_condominios():
    # Seleciona todas as colunas necessárias para a lista e edição
    comando = "SELECT cnpj, nome, logradouro, bairro, cidade, uf, cep FROM CONDOMINIO" 
    try:
        cursor.execute(comando)
        # Retorna tuplas com 7 elementos: (cnpj, nome, logradouro, bairro, cidade, uf, cep)
        resultados = cursor.fetchall() 
        return resultados
    except mysql.connector.Error as err:
        print(f"Erro ao consultar condomínios: {err}")
        return []

def obter_condominio_por_cnpj(cnpj):
    # Seleciona todos os campos EDITÁVEIS, exceto o CNPJ
    comando = "SELECT nome, logradouro, bairro, cidade, uf, cep FROM CONDOMINIO WHERE cnpj = %s"
    try:
        cursor.execute(comando, (cnpj,))
        resultado = cursor.fetchone()
        # Retorna a tupla (nome, logradouro, bairro, cidade, uf, cep)
        return resultado 
    except mysql.connector.Error as err:
        st.error(f"Erro ao buscar condomínio: {err}")
        return None

def atualizar_condominio(cnpj_original, novo_nome, novo_logradouro, novo_bairro, nova_cidade, nova_uf, novo_cep):
    comando = """
    UPDATE CONDOMINIO SET 
        nome = %s, logradouro = %s, bairro = %s, 
        cidade = %s, uf = %s, cep = %s 
    WHERE cnpj = %s
    """
    # Ordem dos dados deve ser EXATAMENTE a mesma do comando SQL
    dados = (novo_nome, novo_logradouro, novo_bairro, nova_cidade, nova_uf, novo_cep, cnpj_original)
    
    try:
        cursor.execute(comando, dados)
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Erro ao atualizar condomínio: {err}")
        conexao.rollback()
        return False

def deletar_condominio(cnpj):
    try:
        comando = "DELETE FROM CONDOMINIO WHERE cnpj = %s"
        cursor.execute(comando, (cnpj,))
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Erro ao deletar condomínio: {err}")
        conexao.rollback()
        return False

# =========================================================================
# 3. GESTÃO DE ESTADO (STREAMLIT SESSION STATE)
# =========================================================================

# Inicializa o estado da sessão para controle de navegação
if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False
if 'editing_cnpj' not in st.session_state:
    st.session_state.editing_cnpj = None

# Função para sair do modo de edição
def sair_do_modo_edicao():
    st.session_state.edit_mode = False
    st.session_state.editing_cnpj = None
    st.rerun()

# Carrega os dados mais recentes (executado a cada rerun)
lista_condominios = listar_condominios()

# =========================================================================
# 4. PAINEL DO ADMINISTRADOR (Sempre visível)
# =========================================================================

with st.container(border=True):
    col_icon, col_inf, col_editar, col_sair = st.columns([0.8, 4, 0.5, 0.5], vertical_alignment="center")

    with col_icon:
        st.image("../img/user5.png", width=70) 

    with col_inf:
        st.markdown(f"**{admin_name}**")
        st.caption(f"{admin_email}")

    with col_editar:
        st.button(":material/edit_square:", help="Editar perfil", key="btn_admin_edit")

    with col_sair:
        st.button(":material/logout:", help="Sair da conta", key="btn_admin_sair")


# =========================================================================
# 5. LÓGICA DE EDIÇÃO E LISTAGEM
# =========================================================================

# Painel de condomínios
with st.container(border=True):
    
    # ------------------------------------------------
    # MODO DE EDIÇÃO
    # ------------------------------------------------
    if st.session_state.edit_mode:
        cnpj_para_editar = st.session_state.editing_cnpj
        dados_atuais = obter_condominio_por_cnpj(cnpj_para_editar)

        if dados_atuais:
            # Desempacota a tupla com 6 elementos na ordem: nome, logradouro, bairro, cidade, uf, cep
            nome_atual, logradouro_atual, bairro_atual, cidade_atual, uf_atual, cep_atual = dados_atuais
            
            st.markdown(f"<div style='text-align: center; font-size: 24px;'>Editar Condomínio: {nome_atual}</div>", unsafe_allow_html=True)
            st.caption(f"CNPJ: {cnpj_para_editar}")
            st.write("---")
            
            with st.form("form_edicao_condominio"):
                # Campos pré-preenchidos com os dados atuais
                novo_nome = st.text_input("Nome do Condomínio", value=nome_atual)
                
                # Campos de endereço (seus campos reais)
                novo_logradouro = st.text_input("Logradouro", value=logradouro_atual)
                novo_bairro = st.text_input("Bairro", value=bairro_atual)
                nova_cidade = st.text_input("Cidade", value=cidade_atual)
                nova_uf = st.text_input("UF", value=uf_atual)
                novo_cep = st.text_input("CEP", value=cep_atual)
                
                col_salvar, col_cancelar = st.columns(2)
                
                with col_salvar:
                    salvar = st.form_submit_button("Salvar Alterações", type="primary", use_container_width=True)
                    
            if salvar:
                # 3. Chamada da função com todos os 6 argumentos de dados + o CNPJ de identificação
                if atualizar_condominio(cnpj_para_editar, novo_nome, novo_logradouro, novo_bairro, nova_cidade, nova_uf, novo_cep):
                    st.success(f"Condomínio **{novo_nome}** atualizado com sucesso!")
                    sair_do_modo_edicao()
            st.button("Cancelar", on_click=sair_do_modo_edicao, use_container_width=True) 
   
        else:
            st.error(f"Condomínio com CNPJ '{cnpj_para_editar}' não encontrado para edição.")
            st.button("Voltar para Lista", on_click=sair_do_modo_edicao)

    # ------------------------------------------------
    # MODO DE LISTAGEM (NÃO ESTÁ EDITANDO)
    # ------------------------------------------------
    else:
        st.markdown("<div style='text-align: center; font-size: 24px;'>Condomínios</div>", unsafe_allow_html=True)
        st.write("") 

        barra_pesquisar = st.text_input("Buscar", placeholder="🔍 Digite o nome do condomínio...", label_visibility="collapsed")
        st.write("")

        # Lista de condomínios
        with st.container(height=300, border=False):
            # O loop agora itera sobre a lista que contém (CNPJ, Nome, Logradouro, ...)
            for condominio in lista_condominios:
                cnpj_condominio = condominio[0] # CNPJ
                nome_condominio = condominio[1] # Nome
                
                with st.container(border=True):
                    col_icon, col_nome, col_inf , col_editar, col_del = st.columns([0.5, 4, 0.5, 0.5, 0.5], vertical_alignment="center")
                    
                    with col_icon:
                        st.image("../img/condominio.png")
                        
                    with col_nome:
                        st.write(f"**{nome_condominio}**") # Exibe o nome

                    # Botões de visualizar, editar e excluir
                    with col_inf:
                        st.button(":material/visibility:", key=f"btn_info_{cnpj_condominio}", help="Mais informações")
                    
                    # BOTÃO EDITAR
                    with col_editar:
                        editar_clicked = st.button(":material/edit_square:", key=f"btn_edit_{cnpj_condominio}", help="Editar condomínio")

                        if editar_clicked:
                            # Define o estado de edição e força o reinício (rerun)
                            st.session_state.edit_mode = True
                            st.session_state.editing_cnpj = cnpj_condominio
                            st.rerun()

                    # BOTÃO DELETAR
                    with col_del:
                        deleted_clicked = st.button(":material/delete:", key=f"btn_del_{cnpj_condominio}", help="Excluir condomínio")

                    if deleted_clicked:
                        print(f"Botão de deletar clicado para CNPJ: {cnpj_condominio}")
                        if deletar_condominio(cnpj_condominio):
                            st.success(f"Condomínio {nome_condominio} excluído com sucesso!")
                            st.rerun()

# Botão de cadastro de condomínio (só aparece se não estiver editando)
if not st.session_state.edit_mode:
    cadastrar_condominio = st.button("Cadastrar +", help="Cadastrar novo condomínio", use_container_width=True)

# =========================================================================
# 6. FECHAR CONEXÃO
# =========================================================================

# Fechar conexão para liberar recursos
if 'cursor' in locals() and cursor:
    cursor.close()
if 'conexao' in locals() and conexao:
    conexao.close()