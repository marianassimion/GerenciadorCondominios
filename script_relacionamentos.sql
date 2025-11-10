use condominio;
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

CREATE TABLE CONDOMINIO(
	cnpj 				varchar(16) PRIMARY KEY,
    nome 				varchar(65) NOT NULL,
    endereco			varchar(150) NOT NULL
);

CREATE TABLE ADMINISTRADOR(
	id_administrador 	integer AUTO_INCREMENT PRIMARY KEY,
    email				varchar(65),
    nome 				varchar(65) NOT NULL,
    senha				varchar(20) NOT NULL
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
    data_emissao 		date NOT NULL,
	data_vencimento 	date NOT NULL,
    valor				decimal(10,2),
    status_pagamento	varchar(10),
	id_residencia 		integer,
	FOREIGN KEY(id_residencia) references residencia(id_residencia)
);

CREATE TABLE MULTA (
    id_multa 			INTEGER AUTO_INCREMENT PRIMARY KEY,
	data_emissao 		date NOT NULL,
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


