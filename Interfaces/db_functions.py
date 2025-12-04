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
def criar_condominio(cnpj, id_admin, nome, logradouro, bairro, cidade, uf, cep):
    cursor = conexao.cursor(buffered=True)
    try:
        cmd = "INSERT INTO condominio (cnpj, id_admin, nome,  logradouro, bairro, cidade, uf, cep) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(cmd, (cnpj, id_admin, nome,  logradouro, bairro, cidade, uf, cep))
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

def obter_media_salarial_por_condominio(cnpj):
    try:
        if not conexao.is_connected():
            conexao.reconnect()
        cursor = conexao.cursor()
        
        args = [cnpj, 0] 
        
        result = cursor.callproc("calcular_media_salario_por_condominio", args)
        
        media = result[1] # Pega o segundo argumento (o OUT)
        cursor.close()
        return media if media else 0.0
    
    except Exception as e:
        print(f"Erro ao calcular média: {e}")
        return 0.0
    
def obter_historico_salarios(cpf):
    try:
        if not conexao.is_connected():
            conexao.reconnect()

        cursor = conexao.cursor(dictionary=True)

        query = """
        SELECT salario_antigo, salario_novo, data_alteracao
        FROM LOG_ALTERACAO_SALARIO
        WHERE cpf_empregado = %s
        ORDER BY data_alteracao DESC
        """
        cursor.execute(query, (cpf,))
        resultado = cursor.fetchall()
        cursor.close()

        return resultado

    except Exception as e:
        print(f"Erro ao obter histórico de salários: {e}")
        return []

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
        comando = 'INSERT INTO AVISO(titulo, texto, id_administrador, condominio_cnpj) VALUES (%s, %s, %s, %s)'
        valores = (titulo, texto, id_administrador, condominio_cnpj)
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
def listar_avisos(condominio_cnpj):
    local_conexao = get_db_connection()
    cursor = local_conexao.cursor()
    comando = """
        SELECT aviso.id_aviso, aviso.titulo, aviso.texto, aviso.data_aviso, admin.nome, aviso.condominio_cnpj 
        FROM AVISO AS aviso 
        JOIN ADMINISTRADOR AS admin ON aviso.id_administrador = admin.id_administrador 
        WHERE aviso.condominio_cnpj = %s
        ORDER BY aviso.data_aviso DESC
    """
    try:
        cursor.execute(comando, (condominio_cnpj,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        st.error(f"Erro ao listar avisos: {err}")
        return []
    finally:
        cursor.close()

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

# Residência
def listar_residencias(cnpj_condominio):
    cursor = conexao.cursor() 
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
            busca = f"%{unidade}%"
            cursor.execute(sql, (cnpj_condominio, busca, busca))
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
    cursor = conexao.cursor()
    try:
        sql = "SELECT * FROM RESIDENCIA WHERE id_residencia = %s"
        cursor.execute(sql, (id_residencia,))
        return cursor.fetchone()
    except mysql.connector.Error:
        return None
    finally:
        cursor.close()

def criar_residencia(num_unidade, bloco, tipo, condominio_cnpj):
    cursor = conexao.cursor()
    try:
        sql = """
            INSERT INTO RESIDENCIA (num_unidade, bloco, tipo, condominio_cnpj)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (num_unidade, bloco, tipo, condominio_cnpj))
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        conexao.rollback()
        st.error(f"Erro ao criar residência: {err}")
        return False
    finally:
        cursor.close()

def editar_residencia(id_residencia, num_unidade, bloco, tipo):
    cursor = conexao.cursor()
    try:
        sql = """
            UPDATE RESIDENCIA 
            SET num_unidade = %s, bloco = %s, tipo = %s
            WHERE id_residencia = %s
        """
        cursor.execute(sql, (num_unidade, bloco, tipo, id_residencia))
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        conexao.rollback()
        st.error(f"Erro ao atualizar: {err}")
        return False
    finally:
        cursor.close()

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

# Morador
def listar_moradores_residencia(id_residencia):
    cursor = conexao.cursor()
    try:
        sql = """SELECT cpf, nome, email, sindico FROM MORADOR WHERE id_residencia = %s ORDER BY nome"""
        cursor.execute(sql, (id_residencia,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        st.error(f"Erro ao listar moradores da residência: {err}")
        return []
    finally:
        cursor.close()

def listar_moradores_condominio(cnpj_condominio):
    cursor = conexao.cursor()
    try:
        sql = """SELECT M.cpf, M.nome, M.email, M.sindico, 
                   R.id_residencia, R.num_unidade, R.bloco, R.tipo
            FROM MORADOR M
            JOIN RESIDENCIA R ON M.id_residencia = R.id_residencia
            WHERE R.condominio_cnpj = %s
            ORDER BY R.bloco, R.num_unidade, M.nome"""
        cursor.execute(sql, (cnpj_condominio,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        st.error(f"Erro ao listar moradores: {err}")
        return []
    finally:
        cursor.close()

def obter_morador_por_id(cpf):
    cursor = conexao.cursor()
    try:
        sql = """
            SELECT cpf, nome, email, id_residencia, sindico
            FROM MORADOR
            WHERE cpf = %s
        """
        cursor.execute(sql, (cpf,))
        return cursor.fetchone()
    except mysql.connector.Error as err:
        st.error(f"Erro ao buscar morador: {err}")
        return None
    finally:
        cursor.close()

def criar_morador(cpf, nome, email, id_residencia, sindico=False):
    cursor = conexao.cursor()
    try:
        sql = """
            INSERT INTO MORADOR (cpf, nome, email, id_residencia, sindico)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (cpf, nome, email, id_residencia, sindico))
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Erro ao criar morador: {err}")
        return False
    finally:
        cursor.close()

def editar_morador(cpf, nome, email, id_residencia, sindico):
    cursor = conexao.cursor()
    try:
        sql = """
            UPDATE MORADOR 
            SET nome = %s, email = %s, id_residencia = %s, sindico = %s
            WHERE cpf = %s
        """
        cursor.execute(sql, (nome, email, id_residencia, sindico, cpf))
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Erro ao editar morador: {err}")
        return False
    finally:
        cursor.close()

def deletar_morador(cpf):
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM TELEFONE_MORADOR WHERE cpf_morador = %s", (cpf,))
        cursor.execute("DELETE FROM VEICULO WHERE morador_cpf = %s", (cpf,))
        cursor.execute("DELETE FROM MORADOR WHERE cpf = %s", (cpf,))

        conexao.commit()
        return True

    except mysql.connector.Error as err:
        conexao.rollback()
        st.error(f"Erro ao deletar morador: {err}")
        return False
    finally:
        cursor.close()

# Telefone Morador
def listar_telefones_morador(cpf_morador):
    cursor = conexao.cursor()
    try:
        sql = """
            SELECT id_telefone_morador, numero
            FROM TELEFONE_MORADOR
            WHERE cpf_morador = %s
            ORDER BY id_telefone_morador
        """
        cursor.execute(sql, (cpf_morador,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        st.error(f"Erro ao listar telefones: {err}")
        return []
    finally:
        cursor.close()

def criar_telefone(cpf_morador, numero):
    cursor = conexao.cursor()
    try:
        sql = """
            INSERT INTO TELEFONE_MORADOR (cpf_morador, numero)
            VALUES (%s, %s)
        """
        cursor.execute(sql, (cpf_morador, numero))
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Erro ao cadastrar telefone: {err}")
        return False
    finally:
        cursor.close()

def editar_telefone(id_telefone_morador, novo_numero):
    cursor = conexao.cursor()
    try:
        sql = """
            UPDATE TELEFONE_MORADOR
            SET numero = %s
            WHERE id_telefone_morador = %s
        """
        cursor.execute(sql, (novo_numero, id_telefone_morador))
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Erro ao atualizar telefone: {err}")
        return False
    finally:
        cursor.close()

def deletar_telefone(id_telefone):
    cursor = conexao.cursor()
    try:
        sql = "DELETE FROM TELEFONE_MORADOR WHERE id_telefone_morador = %s"
        cursor.execute(sql, (id_telefone,))
        conexao.commit()
        return True
    except Exception as e:
        print(f"Erro ao deletar: {e}")
        return False
    finally:
        cursor.close()

# Veículo
def listar_veiculos_morador(cpf_morador):
    cursor = conexao.cursor()
    try:
        sql = """
            SELECT placa, modelo, cor
            FROM VEICULO
            WHERE morador_cpf = %s
            ORDER BY modelo
        """
        cursor.execute(sql, (cpf_morador,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        st.error(f"Erro ao listar veículos: {err}")
        return []
    finally:
        cursor.close()

def listar_veiculos_condominio(cnpj_condominio):
    cursor = conexao.cursor()
    try:
        sql = """
            SELECT V.placa, V.modelo, V.cor, 
                   M.nome AS morador, M.cpf AS morador_cpf,
                   R.num_unidade, R.bloco
            FROM VEICULO V
            JOIN MORADOR M ON V.morador_cpf = M.cpf
            JOIN RESIDENCIA R ON M.id_residencia = R.id_residencia
            WHERE R.condominio_cnpj = %s
            ORDER BY R.bloco, R.num_unidade, V.modelo
        """
        cursor.execute(sql, (cnpj_condominio,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        st.error(f"Erro ao listar veículos do condomínio: {err}")
        return []
    finally:
        cursor.close()

def listar_veiculos_residencia(id_residencia):
    cursor = conexao.cursor()
    try:
        sql = """
            SELECT 
                V.placa,
                V.modelo,
                V.cor,
                M.nome AS morador_nome,
                M.cpf AS morador_cpf
            FROM VEICULO V
            JOIN MORADOR M ON V.morador_cpf = M.cpf
            WHERE M.id_residencia = %s
            ORDER BY M.nome, V.modelo
        """
        cursor.execute(sql, (id_residencia,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        st.error(f"Erro ao listar veículos da residência: {err}")
        return []
    finally:
        cursor.close()

def criar_veiculo(placa, modelo, cor, morador_cpf):
    cursor = conexao.cursor()
    try:
        sql = """
            INSERT INTO VEICULO (placa, modelo, cor, morador_cpf)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (placa, modelo, cor, morador_cpf))
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Erro ao cadastrar veículo: {err}")
        return False
    finally:
        cursor.close()

def editar_veiculo(placa, modelo, cor, novo_cpf_morador):
    cursor = conexao.cursor()
    try:
        sql = """
            UPDATE VEICULO
            SET modelo = %s, cor = %s, morador_cpf = %s
            WHERE placa = %s
        """
        cursor.execute(sql, (modelo, cor, novo_cpf_morador, placa))
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Erro ao atualizar veículo: {err}")
        return False
    finally:
        cursor.close()

def deletar_veiculo(placa):
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM VEICULO WHERE placa = %s", (placa,))
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Erro ao deletar veículo: {err}")
        return False
    finally:
        cursor.close()

# Taxa
def listar_taxas_residencia(id_residencia):
    cursor = conexao.cursor()
    try:
        sql = """SELECT * FROM TAXA WHERE id_residencia = %s ORDER BY data_vencimento DESC"""
        cursor.execute(sql, (id_residencia,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        st.error(f"Erro ao listar taxas: {err}")
        return []
    finally:
        cursor.close()

def criar_taxa(data_emissao, data_vencimento, valor, status_pagamento, id_residencia):
    cursor = conexao.cursor()
    try:
        sql = """
            INSERT INTO TAXA (data_emissao, data_vencimento, valor, status_pagamento, id_residencia)
            VALUES (NOW(), %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (data_emissao, data_vencimento, valor, status_pagamento, id_residencia))
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Erro ao criar taxa: {err}")
        return False
    finally:
        cursor.close()

def editar_taxa(id_taxa, data_emissao, data_vencimento, valor, status_pagamento):
    cursor = conexao.cursor()
    try:
        sql = """
            UPDATE TAXA 
            SET data_emissao = %s, data_vencimento = %s, valor = %s, status_pagamento = %s
            WHERE id_taxa = %s
        """
        cursor.execute(sql, (data_emissao, data_vencimento, valor, status_pagamento, id_taxa))
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Erro ao editar taxa: {err}")
        return False
    finally:
        cursor.close()

def deletar_taxa(id_taxa):
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM TAXA WHERE id_taxa = %s", (id_taxa,))
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Erro ao deletar taxa: {err}")
        return False
    finally:
        cursor.close()

# Multa
def listar_multas_residencia(id_residencia):
    cursor = conexao.cursor()
    try:
        sql = """
            SELECT id_multa, data_emissao, data_vencimento, status_pagamento, valor, descricao, id_residencia
            FROM MULTA
            WHERE id_residencia = %s
            ORDER BY data_vencimento DESC
        """
        cursor.execute(sql, (id_residencia,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        st.error(f"Erro ao listar multas: {err}")
        return []
    finally:
        cursor.close()

def criar_multa(data_emissao, data_vencimento, status_pagamento, valor, descricao, id_residencia):
    cursor = conexao.cursor()
    try:
        sql = """
            INSERT INTO MULTA (data_emissao, data_vencimento, status_pagamento, valor, descricao, id_residencia)
            VALUES (NOW(), %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (data_emissao, data_vencimento, status_pagamento, valor, descricao, id_residencia))
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Erro ao criar multa: {err}")
        return False
    finally:
        cursor.close()

def editar_multa(id_multa, data_emissao, data_vencimento, status_pagamento, valor, descricao):
    cursor = conexao.cursor()
    try:
        sql = """
            UPDATE MULTA 
            SET data_emissao = %s, data_vencimento = %s, status_pagamento = %s, valor = %s, descricao = %s
            WHERE id_multa = %s
        """
        cursor.execute(sql, (data_emissao, data_vencimento, status_pagamento, valor, descricao, id_multa))
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Erro ao editar multa: {err}")
        return False
    finally:
        cursor.close()

def deletar_multa(id_multa):
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM MULTA WHERE id_multa = %s", (id_multa,))
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Erro ao deletar multa: {err}")
        return False
    finally:
        cursor.close()

# ==============================================================================
# ENTIDADE: ÁREA COMUM
# ==============================================================================

# --- [CREATE] ---
def criar_area_comum(nome, descricao, capacidade, condominio_cnpj):
    cursor = conexao.cursor()
    try:
        cmd = "INSERT INTO AREA_COMUM (nome, descricao, capacidade, condominio_cnpj) VALUES (%s, %s, %s, %s)"
        cursor.execute(cmd, (nome, descricao, capacidade, condominio_cnpj))
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Erro ao criar área comum: {err}")
        return False
    finally:
        cursor.close()

# --- [READ] ---
def obter_area_comum(id_a):
    cursor = conexao.cursor(buffered=True)
    comando = "SELECT nome, descricao, capacidade FROM AREA_COMUM WHERE id_area_comum = %s"
    try:
        cursor.execute(comando, (id_a,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        st.error(f"Erro ao buscar áreas comuns: {err}")
        return None
    finally:
        cursor.close()

def listar_areas_comuns(condominio_cnpj):
    local_conexao = get_db_connection()
    cursor = local_conexao.cursor()
    comando = """SELECT id_area_comum, nome, descricao, capacidade FROM AREA_COMUM WHERE condominio_cnpj = %s """
    try:
        cursor.execute(comando, (condominio_cnpj, ))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        st.error(f"Erro ao listar áreas comuns: {err}")
        return []
    finally:
        cursor.close()

# --- [UPDATE] ---
def atualizar_area_comum(id_area_comum, nome, descricao, capacidade):
    cursor = conexao.cursor(buffered=True)
    cmd = "UPDATE AREA_COMUM SET nome=%s, descricao=%s, capacidade=%s WHERE id_area_comum=%s"
    try:
        cursor.execute(cmd, (nome, descricao, capacidade, id_area_comum))
        conexao.commit()
        return True
    
    except mysql.connector.Error as err:
        st.error(f"Erro ao atualizar área comum: {err}")
        conexao.rollback()
        return False
    
    finally:
        cursor.close()

# --- [DELETE] ---
def deletar_area_comum(id_area_comum):
    cursor = conexao.cursor(buffered=True)
    try:
        cursor.execute("DELETE FROM AREA_COMUM WHERE id_area_comum=%s", (id_area_comum,))
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Erro ao deletar área comum: {err}")
        conexao.rollback()
        return False
    finally:
        cursor.close()