/*VIEW QUE MOSTRA TODOS OS VEÍCULOS DE UM CONDOMÍNIO*/
CREATE OR REPLACE VIEW vw_veiculos_condominio AS
SELECT 
    c.cnpj AS condominio_cnpj, 
    c.nome AS 'Condomínio',
    CONCAT(r.bloco, ' - ', r.num_unidade) AS 'Unidade',
    m.nome AS 'Proprietario',
    m.cpf AS 'CPF',
    v.modelo AS 'Modelo',
    v.cor AS 'Cor',
    v.placa AS 'Placa'
FROM 
    CONDOMINIO c
    INNER JOIN RESIDENCIA r ON c.cnpj = r.condominio_cnpj
    INNER JOIN MORADOR m ON r.id_residencia = m.id_residencia
    INNER JOIN VEICULO v ON m.cpf = v.morador_cpf;

/*VIEW QUE MOSTRA TODOS OS MORADORES DE UM CONDOMÍNIO*/
CREATE OR REPLACE VIEW vw_moradores_condominio AS
SELECT 
    c.cnpj AS condominio_cnpj, 
    c.nome AS 'Condomínio',
    CONCAT(r.bloco, ' - ', r.num_unidade) AS 'Unidade',
    m.nome AS 'Proprietario',
    m.cpf AS 'CPF',
    v.modelo AS 'Modelo',
    v.cor AS 'Cor',
    v.placa AS 'Placa'
FROM 
    CONDOMINIO c
    INNER JOIN RESIDENCIA r ON c.cnpj = r.condominio_cnpj
    INNER JOIN MORADOR m ON r.id_residencia = m.id_residencia
    INNER JOIN VEICULO v ON m.cpf = v.morador_cpf;


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