import mysql.connector
import streamlit as st
import bcrypt
import time
from pages.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME 
import time

# Conexão com o banco de dados
@st.cache_resource
def get_db_connection():
    try:
        return mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
        )
    except mysql.connector.Error as err:
        st.error(f"Erro ao conectar no MySQL: {err}")
        st.stop()

conexao = get_db_connection()

# Login
def verificar_login(email, senha_digitada):
    cursor = conexao.cursor(buffered=True)
    try:
        comando = "SELECT id_administrador, nome, email, senha FROM ADMINISTRADOR WHERE email = %s"
        cursor.execute(comando, (email,))
        usuario = cursor.fetchone()
        if usuario:
            id_admin, nome, email_db, senha_hash_banco = usuario
            if isinstance(senha_hash_banco, str):
                senha_hash_banco = senha_hash_banco.encode('utf-8')
            if bcrypt.checkpw(senha_digitada.encode('utf-8'), senha_hash_banco):
                return (nome, email_db)
        return None 

    except mysql.connector.Error as err:
        st.error(f"Erro no login: {err}")
        return None
    finally:
        cursor.close()

def login_sessao():
    if not st.session_state.get('logged_in'):
        st.error("Acesso negado. Por favor, faça login.")
        time.sleep(3) 
        st.switch_page("login.py")
        st.stop() 

# Condomínio
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

def criar_condominio(nome, cnpj, logradouro, bairro, cidade, uf, cep):
    cursor = conexao.cursor(buffered=True)
    try:
        cmd = "INSERT INTO condominio (nome, cnpj, logradouro, bairro, cidade, uf, cep) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(cmd, (nome, cnpj, logradouro, bairro, cidade, uf, cep))
        conexao.commit()
        return True
    except mysql.connector.Error:
        conexao.rollback()
        return False
    finally:
        cursor.close()

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

def deletar_condominio(cnpj):
    cursor = conexao.cursor(buffered=True)
    try:
        cursor.execute("DELETE FROM CONDOMINIO WHERE cnpj = %s", (cnpj,))
        cursor.execute("SELECT id_residencia FROM RESIDENCIA WHERE condominio_cnpj = %s", (cnpj,))
        residencias = cursor.fetchall()
        
        for (id_res,) in residencias:
            # Apaga dependências da residência
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

        cursor.execute("DELETE FROM CONDOMINIO WHERE cnpj = %s", (cnpj,))
        
        conexao.commit()
        return True
    
    except mysql.connector.Error as err:
        if err.errno == 1451:  # Foreign key constraint
            st.error("Não é possível excluir este condomínio pois existem registros associados, como empregados, moradores, residências, veículos ou taxas.")
        else:
            st.error(f"Erro ao deletar condomínio: {err}")
        
        conexao.rollback()
        return False
    finally:
        cursor.close()

# Empregado
def criar_empregado(cpf, nome, cargo, matricula, data_admissao, salario, condominio_cnpj):
    cursor = conexao.cursor(buffered=True)
    try:
        cmd = "INSERT INTO EMPREGADO (cpf, nome, cargo, matricula, data_admissao, salario, condominio_cnpj) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(cmd, (cpf, nome, cargo, matricula, data_admissao, salario, condominio_cnpj))
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Erro: {err}")
        conexao.rollback()
        return False
    finally:
        cursor.close()

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

def obter_empregados(condominio_cnpj):
    cursor = conexao.cursor(buffered=True)
    comando = "SELECT nome, cargo, matricula, data_admissao, salario, cpf FROM EMPREGADO WHERE condominio_cnpj = %s"

    try:
        cursor.execute(comando, (condominio_cnpj,))
        resultados = cursor.fetchall()
        return resultados
    
    except mysql.connector.Error as err:
        st.error(f"Erro ao buscar empregados: {err}")
        return None
    
    finally:
        cursor.close()

def obter_empregado_por_cpf(cpf):
    cursor = conexao.cursor(buffered=True)
    try:
        cursor.execute("SELECT nome, cargo, matricula, data_admissao, salario, cpf FROM EMPREGADO WHERE cpf = %s", (cpf,))
        return cursor.fetchone()
    except mysql.connector.Error as err:
        st.error(f"Erro ao buscar empregado: {err}")
        return None
    finally:
        cursor.close()

def atualizar_empregado(cpf_original, nome, cargo, matricula, data_admissao, salario):
    cursor = conexao.cursor(buffered=True)
    try:
        cmd = "UPDATE EMPREGADO SET nome=%s, cargo=%s, matricula=%s, data_admissao=%s, salario=%s WHERE cpf=%s"
        cursor.execute(cmd, (nome, cargo, matricula, data_admissao, salario, cpf_original))
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Erro ao atualizar empregado: {err}")
        conexao.rollback()
        return False
    finally:
        cursor.close()

def criar_aviso(titulo, texto, id_administrador, condominio_cnpj):
    cursor = conexao.cursor(buffered=True)
    try:
        comando = f'INSERT INTO AVISO(titulo, texto, id_administrador) VALUES (%s, %s, %s)'
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


def listar_avisos():
    conexao = get_db_connection()
    cursor = conexao.cursor()
    comando = """SELECT aviso.id_aviso, aviso.titulo, aviso.texto, aviso.data_aviso, admin.nome, aviso.condominio_cnpj   FROM AVISO AS aviso JOIN ADMINISTRADOR AS admin ON aviso.id_administrador = admin.id_administrador ORDER BY aviso.data_aviso DESC"""
    
    try:
        cursor.execute(comando)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        st.error(f"Erro ao listar avisos: {err}")
        return []
    finally:
        cursor.close()



# =========================================================================
# FUNÇÃO DE LOGIN 
# =========================================================================

# def verificar_login(email, senha_digitada):
#     cursor = conexao.cursor(buffered=True)
#     comando = "SELECT nome, cargo, matricula, data_admissao, salario, cpf FROM EMPREGADO WHERE condominio_cnpj = %s"
#     try:
#         cursor.execute(comando, (cnpj_condominio,))
#         return cursor.fetchall()
#     except mysql.connector.Error as err:
#         st.error(f"Erro ao buscar empregados: {err}")
#         return []
#     finally:
#         cursor.close()

# Residência
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
    conexao = get_db_connection()
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
        conexao.close()

def criar_residencia(num_unidade, bloco, tipo, condominio_cnpj):
    cursor = conexao.cursor()
    try:
        cmd = "INSERT INTO RESIDENCIA (num_unidade, bloco, tipo, condominio_cnpj) VALUES (%s, %s, %s, %s)"
        cursor.execute(cmd, (num_unidade, bloco, tipo, condominio_cnpj))
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Erro ao criar: {err}")
        return False
    finally:
        cursor.close()

def editar_residencia(id_residencia, num_unidade, bloco, tipo):
    conexao = get_db_connection()
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
        st.error(f"Erro ao atualizar: {err}")
        return False
    finally:
        cursor.close()

def deletar_residencia(id_residencia):
    conexao = get_db_connection()
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
        st.error(f"Erro ao deletar: {e}")
        return False
    finally:
        cursor.close()