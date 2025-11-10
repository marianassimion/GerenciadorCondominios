SET FOREIGN_KEY_CHECKS = 0; -- Desliga a verificação

DROP TABLE IF EXISTS CONDOMINIO;
DROP TABLE IF EXISTS ADMINISTRADOR;
DROP TABLE IF EXISTS RESIDENCIA;
DROP TABLE IF EXISTS EMPREGADO;
DROP TABLE IF EXISTS AVISO;
DROP TABLE IF EXISTS MORADOR;
DROP TABLE IF EXISTS TELEFONE_MORADOR;
DROP TABLE IF EXISTS VISITANTE;
DROP TABLE IF EXISTS VEICULO;
DROP TABLE IF EXISTS TAXA;
DROP TABLE IF EXISTS MULTA;

SET FOREIGN_KEY_CHECKS = 1; -- Liga a verificação de volta

CREATE TABLE CONDOMINIO(
	cnpj 				varchar(16) PRIMARY KEY,
    nome 				varchar(65) NOT NULL,
    endereco			varchar(150) NOT NULL
);

CREATE TABLE ADMINISTRADOR(
	id_administrador 	integer AUTO_INCREMENT PRIMARY KEY,
    email				varchar(65),
    nome 				varchar(65) NOT NULL,
    senha				varchar(255) NOT NULL #aplicar função hash
);

CREATE TABLE RESIDENCIA(
	id_residencia 		integer AUTO_INCREMENT PRIMARY KEY,
	condominio_cnpj		varchar(16),
    num_unidade			integer unsigned NOT NULL,
	bloco 				varchar(10),
	endereco 			varchar(150) NOT NULL UNIQUE,
	FOREIGN KEY(condominio_cnpj) references CONDOMINIO(cnpj)
);

CREATE TABLE EMPREGADO(
	cpf 				varchar(14) PRIMARY KEY,
    nome 				varchar(65) NOT NULL,
    cargo				varchar(150) NOT NULL,
    matricula 			integer unsigned UNIQUE,
	data_admissao		date NOT NULL,
    salario				decimal(10,2),
    condominio_cnpj		varchar(16),
	FOREIGN KEY(condominio_cnpj) references CONDOMINIO(cnpj)

);

CREATE TABLE AVISO (
    id_aviso INTEGER AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(50),
    texto VARCHAR(220),
    data_aviso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_administrador    integer,
    FOREIGN KEY(id_administrador) references ADMINISTRADOR(id_administrador)
);

CREATE TABLE MORADOR(
	cpf 				varchar(14) PRIMARY KEY,
    nome 				varchar(65) NOT NULL,
	email				varchar(65),
	id_residencia 		integer,
	FOREIGN KEY(id_residencia) references RESIDENCIA(id_residencia)
);


CREATE TABLE TELEFONE_MORADOR(
	id_telefone_morador		INT PRIMARY KEY auto_increment,
    cpf 					varchar(14),
    numero					varchar(20),
    foreign key(cpf) references MORADOR(cpf) ON DELETE CASCADE
);


CREATE TABLE VEICULO(
	placa 				varchar(10) PRIMARY KEY,
	modelo 				varchar(40) NOT NULL,
	cor 				varchar(14),
    morador_cpf			varchar(14),
	FOREIGN KEY(morador_cpf) references MORADOR(cpf)
);

CREATE TABLE TAXA(
	id_taxa 			INTEGER AUTO_INCREMENT PRIMARY KEY,
    data_emissao 		date NOT NULL DEFAULT (CURRENT_DATE),
	data_vencimento 	DATE AS (DATE_ADD(data_emissao, INTERVAL 30 DAY)) STORED,
    valor				decimal(10,2),
    status_pagamento	varchar(10),
    descricao 			VARCHAR(220),
	id_residencia 		integer,
	FOREIGN KEY(id_residencia) references residencia(id_residencia)
);

CREATE TABLE MULTA (
    id_multa 			INTEGER AUTO_INCREMENT PRIMARY KEY,
    data_emissao 		date NOT NULL DEFAULT (CURRENT_DATE),
	status_pagamento	varchar(10),
    valor 				DECIMAL(10, 2),
    descricao 			VARCHAR(220),
	id_residencia 		integer,
	FOREIGN KEY(id_residencia) references residencia(id_residencia)
);


CREATE TABLE VISITANTE(
    id_visitante        INTEGER AUTO_INCREMENT PRIMARY KEY,
    rg   				varchar(14),
    nome 				varchar(65) NOT NULL,
    data_entrada        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_residencia 		integer,
	FOREIGN KEY(id_residencia) references RESIDENCIA(id_residencia)
);

INSERT INTO CONDOMINIO (cnpj, nome, endereco) VALUES 
('11222333000144', 'Condomínio Vila Verde', 'Rua das Flores, 123, Bairro Feliz');

-- 5. ADMINISTRADORES (Tabelas "Mãe")
-- (Os IDs 1 e 2 serão gerados automaticamente)
-- ATENÇÃO: A senha 'admin123' SÓ FUNCIONA se a sua coluna for varchar(20).
-- O CORRETO é a coluna ser varchar(255) e a senha ser um HASH.
INSERT INTO ADMINISTRADOR (email, nome, senha) VALUES
('admin@condo.com', 'Administrador Padrão', 'admin123'),
('sindico@condo.com', 'Maria Síndica', 'senha123');

-- 6. RESIDÊNCIAS (Depende de CONDOMINIO)
-- (Os IDs 1, 2, 3 serão gerados automaticamente)
INSERT INTO RESIDENCIA (condominio_cnpj, num_unidade, bloco, endereco) VALUES
('11222333000144', 101, 'A', 'Rua das Flores, 123 - Apto 101 A'),
('11222333000144', 102, 'A', 'Rua das Flores, 123 - Apto 102 A'),
('11222333000144', 201, 'B', 'Rua das Flores, 123 - Apto 201 B');

-- 7. EMPREGADOS (Depende de CONDOMINIO)
INSERT INTO EMPREGADO (cpf, nome, cargo, matricula, data_admissao, salario, condominio_cnpj) VALUES
('11122233344', 'Carlos Porteiro', 'Porteiro Diurno', 1001, '2022-05-10', 2100.00, '11222333000144'),
('22233344455', 'João Zelador', 'Zelador', 1002, '2021-03-15', 2300.00, '11222333000144');

-- 8. AVISOS (Depende de ADMINISTRADOR)
-- (Os IDs serão gerados automaticamente; as datas também)
INSERT INTO AVISO (titulo, texto, id_administrador) VALUES
('Manutenção Piscina', 'A piscina estará fechada para manutenção nos dias 15 e 16.', 1),
('Reunião Condomínio', 'Haverá reunião geral no salão de festas dia 20 às 19h.', 2);

-- 9. MORADORES (Depende de RESIDENCIA)
INSERT INTO MORADOR (cpf, nome, email, id_residencia) VALUES
('12345678901', 'Ana Silva', 'ana.silva@email.com', 1),  -- Mora na Residência 1 (Apto 101A)
('98765432101', 'Bruno Costa', 'bruno.costa@email.com', 1), -- Mora na Residência 1 (Apto 101A)
('55566677788', 'Carla Dias', 'carla.dias@email.com', 2),    -- Mora na Residência 2 (Apto 102A)
('12312312312', 'Daniel Moreira', 'daniel.moreira@email.com', 3); -- Mora na Residência 3 (Apto 201B)

-- 10. TELEFONES (Depende de MORADOR)
INSERT INTO TELEFONE_MORADOR (cpf, numero) VALUES
('12345678901', '(61) 99999-1111'),
('98765432101', '(61) 98888-2222'),
('55566677788', '(21) 97777-3333');

-- 11. VEÍCULOS (Depende de MORADOR)
INSERT INTO VEICULO (placa, modelo, cor, morador_cpf) VALUES
('JJK1A23', 'Honda Civic', 'Prata', '12345678901'), -- Veículo da Ana
('BRA2E19', 'Fiat Uno', 'Branco', '55566677788');  -- Veículo da Carla

-- 12. TAXAS (Depende de RESIDENCIA)
-- (As datas são automáticas pela estrutura da tabela)
INSERT INTO TAXA (valor, status_pagamento, descricao, id_residencia) VALUES
(550.00, 'Pendente', 'Taxa Condominial Mês 11', 1), -- Para o Apto 101A
(550.00, 'Pago', 'Taxa Condominial Mês 10', 1),     -- Para o Apto 101A
(550.00, 'Pendente', 'Taxa Condominial Mês 11', 2), -- Para o Apto 102A
(650.00, 'Pendente', 'Taxa Condominial Mês 11 (Cobertura)', 3); -- Para o Apto 201B

-- 13. MULTAS (Depende de RESIDENCIA)
-- (A data de emissão é automática)
INSERT INTO MULTA (status_pagamento, valor, descricao, id_residencia) VALUES
('Pendente', 150.00, 'Barulho excessivo após as 22h (dia 1)', 1), -- Para o Apto 101A
('Pendente', 80.00, 'Uso indevido do elevador de serviço', 3);   -- Para o Apto 201B

-- 14. VISITANTES (Depende de RESIDENCIA)
-- (A data de entrada é automática)
INSERT INTO VISITANTE (rg, nome, id_residencia) VALUES
('MG-12.345.678', 'Visitante Teste 1', 2), -- Visitante para o Apto 102A
('SP-98.765.432', 'Visitante Teste 2', 2); -- Visitante para o Apto 102A
