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

