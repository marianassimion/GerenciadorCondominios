import streamlit as st
import mysql.connector
from pages.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME 

# =========================================================================
# CONEXÃO COM O BANCO DE DADOS
# =========================================================================
@st.cache_resource
def get_db_connection():
    try:
        return mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
        )
    except mysql.connector.Error as err:
        st.error(f"Erro de conexão: {err}")
        st.stop()

def criar_condominio(nome, cnpj, logradouro, bairro, cidade, uf, cep):
    conexao = get_db_connection()
    cursor = conexao.cursor()
    try:
        cmd = "INSERT INTO condominio (nome, cnpj, logradouro, bairro, cidade, uf, cep) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(cmd, (nome, cnpj, logradouro, bairro, cidade, uf, cep))
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Erro ao criar: {err}")
        conexao.rollback()
        return False
    finally:
        cursor.close()

def listar_condominios():
    conexao = get_db_connection()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT cnpj, nome, logradouro, bairro, cidade, uf, cep FROM CONDOMINIO")
        return cursor.fetchall()
    except mysql.connector.Error as err:
        st.error(f"Erro: {err}")
        return []


def deletar_condominio(cnpj):
    conexao = get_db_connection()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM CONDOMINIO WHERE cnpj = %s", (cnpj,))
        conexao.commit()
        return True
    except mysql.connector.Error:
        conexao.rollback()
        return False
    
def obter_condominio_por_cnpj(cnpj):
    conexao = get_db_connection()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT nome, logradouro, bairro, cidade, uf, cep FROM CONDOMINIO WHERE cnpj = %s", (cnpj,))
        return cursor.fetchone()
    except mysql.connector.Error as err:
        st.error(f"Erro ao buscar condomínio: {err}")
        return None
    finally:
        cursor.close()

def atualizar_condominio(cnpj_original, nome, logradouro, bairro, cidade, uf, cep):
    conexao = get_db_connection()
    cursor = conexao.cursor()
    try:
        cmd = """
            UPDATE CONDOMINIO 
            SET nome=%s, logradouro=%s, bairro=%s, cidade=%s, uf=%s, cep=%s 
            WHERE cnpj=%s
        """
        cursor.execute(cmd, (nome, logradouro, bairro, cidade, uf, cep, cnpj_original))
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Erro ao atualizar: {err}")
        conexao.rollback()
        return False
    finally:
        cursor.close()

def criar_empregado(cpf, nome, cargo, matricula, data_admissao, salario, condominio_cnpj):
    conexao = get_db_connection()
    cursor = conexao.cursor()

    try:
        cmd = "INSERT INTO EMPREGADO (cpf, nome, cargo, matricula, data_admissao, salario, condominio_cnpj) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(cmd, (cpf, nome, cargo, matricula, data_admissao, salario, condominio_cnpj))
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Erro ao cadastrar empregado: {err}")
        conexao.rollback()
        return False
    

def obter_empregado_por_cpf(cpf):
    conexao = get_db_connection()
    cursor = conexao.cursor()
    try:
        # Busca todos os dados do empregado pelo CPF
        cursor.execute("SELECT nome, cargo, matricula, data_admissao, salario, cpf FROM EMPREGADO WHERE cpf = %s", (cpf,))
        return cursor.fetchone()
    except mysql.connector.Error as err:
        st.error(f"Erro ao buscar empregado: {err}")
        return None
    finally:
        cursor.close()

def atualizar_empregado(cpf_original, nome, cargo, matricula, data_admissao, salario):
    conexao = get_db_connection()
    cursor = conexao.cursor()
    try:
        # Atualiza os dados (O CPF geralmente não mudamos pois é a chave primária)
        cmd = """
            UPDATE EMPREGADO 
            SET nome=%s, cargo=%s, matricula=%s, data_admissao=%s, salario=%s 
            WHERE cpf=%s
        """
        cursor.execute(cmd, (nome, cargo, matricula, data_admissao, salario, cpf_original))
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Erro ao atualizar empregado: {err}")
        conexao.rollback()
        return False
    finally:
        cursor.close()
        
def obter_empregados(cnpj_condominio):
    conexao = get_db_connection()
    cursor = conexao.cursor()
    try:
        comando = "SELECT nome, cargo, matricula, data_admissao, salario, cpf FROM EMPREGADO WHERE condominio_cnpj = %s"
        cursor.execute(comando, (cnpj_condominio,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        st.error(f"Erro ao buscar empregados: {err}")
        return []


def deletar_condominio(cnpj):
    conexao = get_db_connection()
    cursor = conexao.cursor()
    try:
        comando = "DELETE FROM CONDOMINIO WHERE cnpj = %s"
        cursor.execute(comando, (cnpj,))
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Erro ao deletar condomínio: {err}")
        conexao.rollback()
        return False


def obter_empregados(cnpj):
    conexao = get_db_connection()
    cursor = conexao.cursor()
    try:
        comando = "SELECT nome, cargo, matricula, data_admissao, salario, cpf FROM EMPREGADO WHERE condominio_cnpj = %s"
        cursor.execute(comando, (cnpj, ))
        resultado = cursor.fetchall()
        return resultado
    except mysql.connector.Error as err:
        st.error(f"Erro ao buscar empregados: {err}")
        return None

def deletar_empregado(cpf):
    conexao = get_db_connection()
    cursor = conexao.cursor()
    try:
        comando = "DELETE FROM EMPREGADO WHERE cpf = %s"
        cursor.execute(comando, (cpf,))
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Erro ao deletar empregado: {err}")
        conexao.rollback()
        return False