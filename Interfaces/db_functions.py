import streamlit as st
import mysql.connector
import bcrypt
import time
from pages.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME 

# ==============================================================================
# CONFIGURAÇÃO E CONEXÃO COM BANCO DE DADOS
# ==============================================================================

@st.cache_resource
def get_db_connection():
    """Estabelece a conexão com o banco de dados MySQL."""
    try:
        return mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
        )
    except mysql.connector.Error as err:
        st.error(f"Erro ao conectar no MySQL: {err}")
        st.stop()

# Inicializa a conexão global (cuidado ao usar globalmente em apps multi-thread)
conexao = get_db_connection()


# ==============================================================================
# AUTENTICAÇÃO E SESSÃO
# ==============================================================================

def verificar_login(email, senha_digitada):
    """Verifica as credenciais do administrador no banco."""
    cursor = conexao.cursor(buffered=True)
    try:
        comando = "SELECT id_administrador, nome, email, senha FROM ADMINISTRADOR WHERE email = %s"
        cursor.execute(comando, (email,))
        usuario = cursor.fetchone()
        
        if usuario:
            id_admin, nome, email_db, senha_hash_banco = usuario
            
            # Garante que o hash esteja em bytes
            if isinstance(senha_hash_banco, str):
                senha_hash_banco = senha_hash_banco.encode('utf-8')
            
            # Compara a senha digitada com o hash
            if bcrypt.checkpw(senha_digitada.encode('utf-8'), senha_hash_banco):
                return (id_admin, nome, email_db)
        
        return None 

    except mysql.connector.Error as err:
        st.error(f"Erro no login: {err}")
        return None
    finally:
        cursor.close()

def login_sessao():
    """Gerencia o estado da sessão e redirecionamento."""
    if not st.session_state.get('logged_in'):
        st.error("Acesso negado. Por favor, faça login.")
        time.sleep(3) 
        st.switch_page("login.py")
        st.stop() 


# ==============================================================================
# ENTIDADE: CONDOMÍNIO
# ==============================================================================

# --- [CREATE] ---
def criar_condominio(nome, id_admin, cnpj, logradouro, bairro, cidade, uf, cep):
    cursor = conexao.cursor(buffered=True)
    try:
        cmd = "INSERT INTO condominio (nome, id_admin, cnpj, logradouro, bairro, cidade, uf, cep) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(cmd, (nome, id_admin, cnpj, logradouro, bairro, cidade, uf, cep))
        conexao.commit()
        return True
    except mysql.connector.Error:
        conexao.rollback()
        return False
    finally:
        cursor.close()

# --- [READ] ---
def listar_condominios():
    cursor = conexao.cursor(buffered=True) 
    try:
        cursor.execute("SELECT cnpj, nome, logradouro, bairro, cidade, uf, cep FROM CONDOMINIO")
        return cursor.fetchall()
    except mysql.connector.Error as err:
        st.error(f"Erro: {err}")
        return []
    finally:
        cursor.close()

def obter_condominio_por_cnpj(cnpj):
    cursor = conexao.cursor(buffered=True)
    try:
        cursor.execute("SELECT nome, logradouro, bairro, cidade, uf, cep FROM CONDOMINIO WHERE cnpj = %s", (cnpj,))
        return cursor.fetchone()
    except mysql.connector.Error:
        return None
    finally:
        cursor.close()

# --- [UPDATE] ---
def atualizar_condominio(cnpj_original, nome, logradouro, bairro, cidade, uf, cep):
    cursor = conexao.cursor(buffered=True)
    try:
        cmd = "UPDATE CONDOMINIO SET nome=%s, logradouro=%s, bairro=%s, cidade=%s, uf=%s, cep=%s WHERE cnpj=%s"
        cursor.execute(cmd, (nome, logradouro, bairro, cidade, uf, cep, cnpj_original))
        conexao.commit()
        return True
    except mysql.connector.Error:
        conexao.rollback()
        return False
    finally:
        cursor.close()

# --- [DELETE] ---
def deletar_condominio(cnpj):
    cursor = conexao.cursor(buffered=True)
    try:
        # Excluir dependências em cascata manualmente
        cursor.execute("SELECT id_residencia FROM RESIDENCIA WHERE condominio_cnpj = %s", (cnpj,))
        residencias = cursor.fetchall()

        for (id_res,) in residencias:
            cursor.execute("DELETE FROM MULTA WHERE id_residencia = %s", (id_res,))
            cursor.execute("DELETE FROM TAXA WHERE id_residencia = %s", (id_res,))
            cursor.execute("DELETE FROM VISITANTE WHERE id_residencia = %s", (id_res,))

            cursor.execute("SELECT cpf FROM MORADOR WHERE id_residencia = %s", (id_res,))
            moradores = cursor.fetchall()

            for (cpf_morador,) in moradores:
                cursor.execute("DELETE FROM VEICULO WHERE morador_cpf = %s", (cpf_morador,))
                cursor.execute("DELETE FROM TELEFONE_MORADOR WHERE cpf = %s", (cpf_morador,))

            cursor.execute("DELETE FROM MORADOR WHERE id_residencia = %s", (id_res,))
            cursor.execute("DELETE FROM RESIDENCIA WHERE id_residencia = %s", (id_res,))

        cursor.execute("DELETE FROM EMPREGADO WHERE condominio_cnpj = %s", (cnpj,))
        cursor.execute("DELETE FROM CONDOMINIO WHERE cnpj = %s", (cnpj,))

        conexao.commit()
        return True

    except mysql.connector.Error as err:
        if err.errno == 1451:
            st.error(
                "Não é possível excluir este condomínio pois possui dependências associadas. "
                "Limpe os dados associados antes de excluir."
            )
        else:
            st.error(f"Erro ao deletar condomínio: {err}")
        
        conexao.rollback()
        return False

    finally:
        cursor.close()


# ==============================================================================
# ENTIDADE: EMPREGADO
# ==============================================================================

# --- [CREATE] ---
def criar_empregado(cpf, nome, cargo, matricula, data_admissao, salario, cnpj_atual, foto_bytes):
    cursor = conexao.cursor(buffered=True)
    query = """
        INSERT INTO EMPREGADO
        (cpf, nome, cargo, matricula, data_admissao, salario, condominio_cnpj, foto)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (cpf, nome, cargo, matricula, data_admissao, salario, cnpj_atual, foto_bytes))
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Erro ao criar empregado: {err}")
        conexao.rollback()
        return False
    finally:
        cursor.close()

# --- [READ] ---
def obter_empregados(condominio_cnpj):
    cursor = conexao.cursor(buffered=True)
    comando = "SELECT nome, cargo, matricula, data_admissao, salario, cpf, foto FROM EMPREGADO WHERE condominio_cnpj = %s"
    try:
        cursor.execute(comando, (condominio_cnpj,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        st.error(f"Erro ao buscar empregados: {err}")
        return None
    finally:
        cursor.close()

def obter_empregado_por_cpf(cpf):
    cursor = conexao.cursor(buffered=True)
    try:
        cursor.execute("SELECT nome, cargo, matricula, data_admissao, salario, cpf, foto FROM EMPREGADO WHERE cpf = %s", (cpf,))
        return cursor.fetchone()
    except mysql.connector.Error as err:
        st.error(f"Erro ao buscar empregado: {err}")
        return None
    finally:
        cursor.close()

# --- [UPDATE] ---
def atualizar_empregado(nome, cargo, matricula, data_admissao, salario, foto, cpf_original):
    cursor = conexao.cursor(buffered=True)
    try:
        if foto is None:
            cursor.execute("SELECT foto FROM EMPREGADO WHERE cpf=%s", (cpf_original,))
            foto_atual = cursor.fetchone()[0]
            foto = foto_atual
        
        cmd = "UPDATE EMPREGADO SET nome=%s, cargo=%s, matricula=%s, data_admissao=%s, salario=%s, foto=%s WHERE cpf=%s"
        cursor.execute(cmd, (nome, cargo, matricula, data_admissao, salario, foto, cpf_original))
        conexao.commit()
        return True
    
    except mysql.connector.Error as err:
        st.error(f"Erro ao atualizar empregado: {err}")
        conexao.rollback()
        return False
    
    finally:
        cursor.close()

# --- [DELETE] ---
def deletar_empregado(cpf):
    cursor = conexao.cursor(buffered=True)
    try:
        cursor.execute("DELETE FROM EMPREGADO WHERE cpf = %s", (cpf,))
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Erro ao deletar empregado: {err}")
        conexao.rollback()
        return False
    finally:
        cursor.close()


# ==============================================================================
# ENTIDADE: AVISOS
# ==============================================================================

# --- [CREATE] ---
def criar_aviso(titulo, texto, id_administrador, condominio_cnpj):
    cursor = conexao.cursor(buffered=True)
    try:
        comando = 'INSERT INTO AVISO(titulo, texto, id_administrador) VALUES (%s, %s, %s)'
        valores = (titulo, texto, id_administrador)
        cursor.execute(comando, valores)
        conexao.commit()
        print(f"Aviso '{titulo}' criado com sucesso!")
        return True
    except mysql.connector.Error as err:
        print(f"Erro ao criar aviso: {err}")
        conexao.rollback()
        return False
    finally:
        cursor.close()

# --- [READ] ---
def listar_avisos():
    # Nota: Aqui cria-se uma nova conexão/cursor, independente da global
    local_conexao = get_db_connection()
    cursor = local_conexao.cursor()
    comando = """
        SELECT aviso.id_aviso, aviso.titulo, aviso.texto, aviso.data_aviso, admin.nome, aviso.condominio_cnpj 
        FROM AVISO AS aviso 
        JOIN ADMINISTRADOR AS admin ON aviso.id_administrador = admin.id_administrador 
        ORDER BY aviso.data_aviso DESC
    """
    try:
        cursor.execute(comando)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        st.error(f"Erro ao listar avisos: {err}")
        return []
    finally:
        cursor.close()
        # É boa prática fechar a conexão local se não for reutilizada, 
        # mas como é get_db_connection com cache, o streamlit gerencia.

# --- [DELETE] ---
def deletar_aviso(id_aviso):
    cursor = conexao.cursor(buffered=True)
    try:
        cursor.execute("DELETE FROM AVISO WHERE id_aviso = %s", (id_aviso,))
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Erro ao deletar aviso: {err}")
        conexao.rollback()
        return False
    finally:
        cursor.close()


# ==============================================================================
# ENTIDADE: RESIDÊNCIA
# ==============================================================================

# --- [CREATE] ---
def criar_residencia(num_unidade, bloco, tipo, condominio_cnpj):
    cursor = conexao.cursor()
    try:
        cmd = "INSERT INTO RESIDENCIA (num_unidade, bloco, tipo, condominio_cnpj) VALUES (%s, %s, %s, %s)"
        cursor.execute(cmd, (num_unidade, bloco, tipo, condominio_cnpj))
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Erro ao criar residência: {err}")
        return False
    finally:
        cursor.close()

# --- [READ] ---
def listar_residencias(cnpj_condominio):
    cursor = conexao.cursor(buffered=True) 
    try:
        sql = """
            SELECT id_residencia, num_unidade, bloco, tipo 
            FROM RESIDENCIA 
            WHERE condominio_cnpj = %s
            ORDER BY bloco, num_unidade
        """
        cursor.execute(sql, (cnpj_condominio,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        st.error(f"Erro ao buscar residências: {err}")
        return []
    finally:
        cursor.close()

def buscar_residencias(cnpj_condominio, unidade=""):
    cursor = conexao.cursor(dictionary=True) 
    try:
        if unidade:
            sql = """
                SELECT id_residencia, num_unidade, bloco, tipo 
                FROM RESIDENCIA 
                WHERE condominio_cnpj = %s 
                AND (CAST(num_unidade AS CHAR) LIKE %s OR bloco LIKE %s)
                ORDER BY bloco, num_unidade
            """
            busca_unidade = f"%{unidade}%"
            cursor.execute(sql, (cnpj_condominio, busca_unidade, busca_unidade))
        else:
            sql = """
                SELECT id_residencia, num_unidade, bloco, tipo 
                FROM RESIDENCIA 
                WHERE condominio_cnpj = %s
                ORDER BY bloco, num_unidade
            """
            cursor.execute(sql, (cnpj_condominio,))
            
        return cursor.fetchall()
    
    except mysql.connector.Error as err:
        st.error(f"Erro ao buscar residências: {err}")
        return []
    finally:
        cursor.close()

def obter_residencia_por_id(id_residencia):
    cursor = conexao.cursor(buffered=True)
    try:
        # Nota: Corrigi a tabela de CONDOMINIO para RESIDENCIA, pois parecia um erro lógico
        cursor.execute("SELECT num_unidade, bloco, tipo, condominio_cnpj FROM RESIDENCIA WHERE id_residencia = %s", (id_residencia,))
        return cursor.fetchone()
    except mysql.connector.Error:
        return None
    finally:
        cursor.close()

# --- [UPDATE] ---
def editar_residencia(id_residencia, num_unidade, bloco, tipo):
    cursor = conexao.cursor()
    try:
        cmd = """
            UPDATE RESIDENCIA 
            SET num_unidade = %s, bloco = %s, tipo = %s 
            WHERE id_residencia = %s
        """
        cursor.execute(cmd, (num_unidade, bloco, tipo, id_residencia))
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Erro ao atualizar residência: {err}")
        return False
    finally:
        cursor.close()

# --- [DELETE] ---
def deletar_residencia(id_residencia):
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM MULTA WHERE id_residencia = %s", (id_residencia,))
        cursor.execute("DELETE FROM TAXA WHERE id_residencia = %s", (id_residencia,))
        cursor.execute("UPDATE MORADOR SET id_residencia = NULL WHERE id_residencia = %s", (id_residencia,))
        cursor.execute("DELETE FROM RESIDENCIA WHERE id_residencia = %s", (id_residencia,))
        
        conexao.commit()
        return True
    except Exception as e:
        conexao.rollback() 
        st.error(f"Erro ao deletar residência: {e}")
        return False
    finally:
        cursor.close()


# ==============================================================================
# ENTIDADE: MORADOR
# ==============================================================================

# --- [DELETE] ---
def deletar_morador(cpf):
    cursor = conexao.cursor(buffered=True)
    try:
        cursor.execute("DELETE FROM TELEFONE_MORADOR WHERE cpf_morador = %s", (cpf,))
        cursor.execute("DELETE FROM VEICULO WHERE morador_cpf = %s", (cpf,))
        cursor.execute("DELETE FROM MORADOR WHERE cpf = %s", (cpf,))
        
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        conexao.rollback()
        st.error(f"Erro ao excluir morador: {err}")
        return False
    finally:
        cursor.close()