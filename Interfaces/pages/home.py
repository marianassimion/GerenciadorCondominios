import streamlit as st
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME 


# =========================================================================
# CONEXÃO COM O BANCO DE DADOS
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
    #interromper a execução do Streamlit
    st.stop()


# =========================================================================
# VARIÁVEIS E FUNÇÕES DE GESTÃO DE DADOS
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

def criar_condominio(nome, cnpj, logradouro, bairro, cidade, uf, cep):
    comando = f'INSERT INTO condominio (nome, cnpj, logradouro, bairro, cidade, uf, cep) VALUES (%s, %s, %s, %s, %s, %s, %s)'
    valores = (nome, cnpj, logradouro, bairro, cidade, uf, cep)

    try:
        cursor.execute(comando, valores) # Executa o comando seguro
        conexao.commit()                 # Salva as alterações
        print(f"Condomínio '{nome}' criado com sucesso!")

    except mysql.connector.Error as err:
        print(f"Erro ao inserir condomínio: {err}")
        conexao.rollback() # Desfaz a operação em caso de erro

    return True

def obter_empregados(cnpj):
    comando = "SELECT nome, cargo, matricula, data_admissao, salario FROM EMPREGADO WHERE condominio_cnpj = %s"

    try:
        cursor.execute(comando, (cnpj, ))
        resultado = cursor.fetchall()
        return resultado
    except mysql.connector.Error as err:
        st.error(f"Erro ao buscar empregados: {err}")
        return None

def criar_empregado(cpf, nome, cargo, matricula, data_admissao, salario, condominio_cnpj):
    comando = f'INSERT INTO EMPREGADO(cpf, nome, cargo, matricula, data_admissao, salario, condominio_cnpj) VALUES (%s, %s, %s, %s, %s, %s, %s)'                                              
    valores = (cpf, nome, cargo, matricula, data_admissao, salario, condominio_cnpj)
    try:
        cursor.execute(comando, valores)
        conexao.commit()
        print(f"Empregado '{nome}' cadastrado com sucesso!")
        return True
    
    except mysql.connector.Error as err:
        print(f"Erro ao inserir empregado: {err}")
        conexao.rollback()


# =========================================================================
# GESTÃO DE ESTADO (STREAMLIT SESSION STATE)
# =========================================================================

# Inicializa o estado da sessão para controle de navegação
if 'edit_condominio_mode' not in st.session_state:
    st.session_state.edit_condominio_mode = False
if 'editing_cnpj' not in st.session_state:
    st.session_state.editing_cnpj = None
if 'create_condominio_mode' not in st.session_state:
    st.session_state.create_condominio_mode = False
if 'details_condominio_mode' not in st.session_state:
    st.session_state.details_condominio_mode = False
if 'detail_cnpj' not in st.session_state:
    st.session_state.detail_cnpj= None
if 'create_empregado_mode' not in st.session_state:
    st.session_state.create_empregado_mode = False

# Funções de navegação para limpar estados
def sair_do_modo_edicao_condominio():
    st.session_state.edit_condominio_mode = False
    st.session_state.editing_cnpj = None
    st.rerun()

def sair_para_listagem_condominio():
    st.session_state.details_condominio_mode = False 
    
    # Limpa as outras (por garantia)
    st.session_state.create_condominio_mode = False
    st.session_state.edit_condominio_mode = False
    
    # Limpa os dados temporários
    st.session_state.editing_cnpj = None
    st.session_state.detail_cnpj = None

def sair_do_modo_criacao_condominio():
    st.session_state.create_condominio_mode = False
    st.rerun()

def sair_do_modo_detalhamento():
    st.session_state.details_condominio_mode = False
    st.session_state.detail_cnpj = None
    st.rerun()

def sair_do_modo_criacao_empregado():
    st.session_state.create_empregado_mode = False
    st.rerun()
# Carrega os dados mais recentes (executado a cada rerun)
lista_condominios = listar_condominios()

# =========================================================================
# LÓGICA DE VISUALIZAÇÃO DE ESTADOS
# =========================================================================

#------------------MODO DE CRIAÇÃO DE CONDOMINIOS------------------

if st.session_state.create_condominio_mode:
    st.button("Voltar para Listagem de Condomínios", on_click=sair_para_listagem_condominio, key="btn_back_create")
    st.title("Cadastro de Novo Condomínio")
    st.write("Preencha os campos abaixo para registrar um novo condomínio no sistema.")
    
    with st.form(key='cadastro_form'):
        nome_condominio_input = st.text_input('Nome do Condomínio')
        cnpj_condominio_input = st.text_input('CNPJ (apenas números)')
        logradouro_condominio_input = st.text_input('Logradouro')
        bairro_condominio_input = st.text_input('Bairro')
        cidade_condominio_input = st.text_input('Cidade')
        uf_condominio_input = st.text_input('UF')
        cep_condominio_input = st.text_input('CEP')
        enviado = st.form_submit_button('Salvar Cadastro', type="primary", use_container_width=True)
    
    if enviado:
        if not nome_condominio_input or not cnpj_condominio_input:
            st.error('Os campos Nome e CNPJ são obrigatórios.')
        else:
            # Chama a função de criação com os dados do formulário
            if criar_condominio(nome_condominio_input, cnpj_condominio_input, logradouro_condominio_input, bairro_condominio_input, cidade_condominio_input, uf_condominio_input, cep_condominio_input):
                st.success('✅ Cadastro realizado com sucesso!')
                # Volta automaticamente para a lista após o sucesso
                st.balloons()
                sair_para_listagem_condominio()

#------------------MODO DE CRIAÇÃO DE EMPREGADO------------------
elif st.session_state.create_empregado_mode:
    st.button("Voltar para a listagem de empregados", on_click = sair_do_modo_criacao_empregado)

    # 1. PEGAR O CNPJ DA SESSÃO (Ele já está salvo aqui!)
    condominio_cnpj = st.session_state.detail_cnpj 

    # 2. BUSCAR O NOME
    dados_condo = obter_condominio_por_cnpj(condominio_cnpj)
    
    # Verifica se achou e pega o nome 
    nome_condominio = dados_condo[0] if dados_condo else "Condomínio não identificado"

    st.title("Cadastro de novo empregado")
    st.write(f"Preencha os campos abaixo para registrar um novo empregado ao Condomínio {nome_condominio}")
    
    with st.form(key='cadastro_empregado_form'):
        cpf_empregado__input = st.text_input('CPF (apenas números)')
        nome_empregado_input = st.text_input('Nome do Empregado')
        cargo_empregado_input = st.text_input('Cargo')
        matricula_empregado_input = st.text_input('Matrícula (apenas números)')
        data_admissao_empregado_input = st.date_input('Data de Admissão')
        salario_empregado_input = st.number_input('Salário')
        enviado_empregado = st.form_submit_button('Salvar Cadastro', type="primary", use_container_width=True)
    
    cancelar_empregado = st.button("Cancelar", on_click=sair_do_modo_criacao_empregado, use_container_width=True) 

    if enviado_empregado:
        if not nome_empregado_input or not cpf_empregado__input:
            st.error('Os campos Nome e CPF são obrigatórios.')
        else:
            cpf_limpo = cpf_empregado__input.replace(".", "").replace("-", "")

            if len(cpf_limpo) > 11:
                st.error("O CPF tem dígitos demais. Digite apenas números.")
            else:
                # Chama a função de criação
                if criar_empregado(cpf_limpo, nome_empregado_input, cargo_empregado_input, matricula_empregado_input, data_admissao_empregado_input, salario_empregado_input, condominio_cnpj):
                    st.success('✅ Cadastro realizado com sucesso!')
                    st.balloons()
                    sair_do_modo_criacao_empregado()


#------------------MODO DE EDIÇÃO DE CONDOMINIO------------------
elif st.session_state.edit_condominio_mode:
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
                
                salvar = st.form_submit_button("Salvar Alterações", type="primary", use_container_width=True)
                    
            if salvar:
                # 3. Chamada da função com todos os 6 argumentos de dados + o CNPJ de identificação
                if atualizar_condominio(cnpj_para_editar, novo_nome, novo_logradouro, novo_bairro, nova_cidade, nova_uf, novo_cep):
                    st.success(f"Condomínio **{novo_nome}** atualizado com sucesso!")
                    sair_do_modo_edicao_condominio()
            st.button("Cancelar", on_click=sair_do_modo_edicao_condominio, use_container_width=True) 
   
        else:
            st.error(f"Condomínio com CNPJ '{cnpj_para_editar}' não encontrado para edição.")
            st.button("Voltar para Lista", on_click=sair_do_modo_edicao_condominio)

#------------------MODO DE DETALHAMENTO DO CONDOMINIO------------------
elif st.session_state.details_condominio_mode:
    st.button("Voltar para Listagem de Condomínios", on_click=sair_para_listagem_condominio, key="btn_back_details")

    cnpj_para_detalhar = st.session_state.detail_cnpj
    dados_condominio = obter_condominio_por_cnpj(cnpj_para_detalhar)
    empregados = obter_empregados(cnpj_para_detalhar)

    if dados_condominio:
        nome_condominio, logradouro, bairro, cidade, uf, cep = dados_condominio
        st.title(f"{nome_condominio}")
        st.caption(f"Logradouro: {logradouro}; Bairro: {bairro}; Cidade: {cidade}; UF: {uf}")

        col_titulo, col_botao = st.columns([2, 1], vertical_alignment="bottom")

        with col_titulo:
            st.header("Empregados")

        with col_botao:
            cadastrar_empregado_clicked = st.button("Cadastrar empregado", key="bton_cadastrar_empregado", help="Cadastrar novo funcionário")

        c1, c2, c3, c4, c5 = st.columns([3, 2, 1, 1.5, 1.5])
        c1.markdown("**Nome**")
        c2.markdown("**Cargo**")
        c3.markdown("**Matrícula**")
        c4.markdown("**Admissão**")
        c5.markdown("**Salário**")            

        if empregados:
            with st.container(height=300, border=False):
               for emp in empregados:
                    # O fetchall retorna uma lista de tuplas, então acessamos por índice
                    # 0=nome, 1=cargo, 2=matricula, 3=data, 4=salario
                    nome_emp = emp[0]
                    cargo_emp = emp[1]
                    mat_emp = emp[2]
                    data_emp = emp[3]
                    sal_emp = emp[4]

                    col_nome, col_cargo, col_matricula, col_data, col_salario = st.columns([3, 2, 1, 1.5, 1.5]) 

                    with col_nome:
                        st.write(nome_emp)
                    with col_cargo:
                        st.write(cargo_emp)
                    with col_matricula:
                        st.write(str(mat_emp))
                    with col_data:
                        st.write(str(data_emp))
                    with col_salario:
                        st.write(f"R$ {sal_emp}")
        else:
            st.info("Nenhum empregado cadastrado neste condomínio.")
        
        if cadastrar_empregado_clicked:
            st.session_state.create_empregado_mode = True
            st.rerun()


#------------------MODO LISTAGEM DE CONDOMINIOS------------------
else:
    # HEADER ADMINISTRADOR
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
    
    with st.container(border=True):
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
                        detalhes_clicked = st.button(":material/visibility:", key=f"btn_info_{cnpj_condominio}", help="Mais informações")

                        if detalhes_clicked:
                            st.session_state.details_condominio_mode = True
                            st.session_state.detail_cnpj = cnpj_condominio
                            st.rerun()
                    
                    # BOTÃO EDITAR
                    with col_editar:
                        editar_clicked = st.button(":material/edit_square:", key=f"btn_edit_{cnpj_condominio}", help="Editar condomínio")

                        if editar_clicked:
                            # Define o estado de edição e força o reinício (rerun)
                            st.session_state.edit_condominio_mode = True
                            st.session_state.editing_cnpj = cnpj_condominio
                            st.rerun()

                    # BOTÃO DELETAR
                    with col_del:
                        deleted_clicked = st.button(":material/delete:", key=f"btn_del_{cnpj_condominio}", help="Excluir condomínio")

                    if deleted_clicked:
                        if deletar_condominio(cnpj_condominio):
                            st.success(f"Condomínio {nome_condominio} excluído com sucesso!")
                            st.rerun()
            cadastrar_clicked = st.button("Cadastrar +",  help="Cadastrar novo condomínio", use_container_width=True)

            if cadastrar_clicked:
                st.session_state.create_condominio_mode = True
                st.rerun()




# =========================================================================
# 6. FECHAR CONEXÃO
# =========================================================================

# Fechar conexão para liberar recursos
if 'cursor' in locals() and cursor:
    cursor.close()
if 'conexao' in locals() and conexao:
    conexao.close()