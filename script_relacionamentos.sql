/*SISTEMA DE GERENCIAMENTO DE CONDOMINIOS*/

CREATE DATABASE IF NOT EXISTS condominio;
USE condominio;

DROP TABLE IF EXISTS TELEFONE_MORADOR; 
DROP TABLE IF EXISTS VEICULO;          
DROP TABLE IF EXISTS TAXA;             
DROP TABLE IF EXISTS MULTA;            
DROP TABLE IF EXISTS AVISO;            
DROP TABLE IF EXISTS EMPREGADO;        
DROP TABLE IF EXISTS AREA_COMUM;       
DROP TABLE IF EXISTS MORADOR;          
DROP TABLE IF EXISTS RESIDENCIA;       
DROP TABLE IF EXISTS CONDOMINIO;       
DROP TABLE IF EXISTS ADMINISTRADOR;


CREATE TABLE ADMINISTRADOR (
    id_administrador integer AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL
);

CREATE TABLE CONDOMINIO (
	cnpj 			varchar(16) PRIMARY KEY,
    id_admin 		INTEGER NOT NULL,
    nome 			varchar(65) NOT NULL,
	logradouro		varchar(100) NOT NULL,
 	bairro			varchar(50) NOT NULL,
 	cidade			varchar(50) NOT NULL,
 	uf				char(2) NOT NULL,
 	cep				varchar(9) NOT NULL,
    
    CONSTRAINT FK_condominio_admin 
        FOREIGN KEY(id_admin) REFERENCES ADMINISTRADOR(id_administrador)
);

CREATE TABLE RESIDENCIA (
    id_residencia INT PRIMARY KEY AUTO_INCREMENT,
    num_unidade INTEGER unsigned NOT NULL, 
    bloco VARCHAR(10),
    tipo VARCHAR(50),
    condominio_cnpj VARCHAR(16),
    
    CONSTRAINT FK_residencia_condominio 
        FOREIGN KEY (condominio_cnpj) REFERENCES CONDOMINIO(cnpj)
);

CREATE TABLE MORADOR (
    cpf VARCHAR(11) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    id_residencia INTEGER,
    sindico BOOLEAN NOT NULL DEFAULT FALSE, 
    
    CONSTRAINT FK_morador_residencia 
        FOREIGN KEY (id_residencia) REFERENCES RESIDENCIA(id_residencia)
);

CREATE TABLE TELEFONE_MORADOR (
    id_telefone_morador INT PRIMARY KEY auto_increment,
    cpf_morador VARCHAR(11),
    numero VARCHAR(20),
    
    CONSTRAINT FK_telefone_morador 
        FOREIGN KEY(cpf_morador) REFERENCES MORADOR(cpf) 
        ON DELETE CASCADE
);

CREATE TABLE EMPREGADO (
    cpf varchar(11) PRIMARY KEY,
    nome varchar(65) NOT NULL,
    cargo varchar(150) NOT NULL,
    matricula integer unsigned UNIQUE,
    data_admissao date NOT NULL,
    salario decimal(10,2),
    condominio_cnpj varchar(16),

    CONSTRAINT FK_empregado_condominio 
        FOREIGN KEY (condominio_cnpj) REFERENCES CONDOMINIO(cnpj)
);

ALTER TABLE empregados ADD COLUMN foto LONGBLOB;

CREATE TABLE VEICULO (
    placa VARCHAR(10) PRIMARY KEY,
    modelo VARCHAR(40) NOT NULL,
    cor VARCHAR(20),
    morador_cpf VARCHAR(11) NOT NULL,
    
    CONSTRAINT veiculo_morador 
        FOREIGN KEY (morador_cpf) REFERENCES MORADOR(cpf)
);

CREATE TABLE TAXA (
    id_taxa INTEGER AUTO_INCREMENT PRIMARY KEY,
    data_emissao date NOT NULL,
    data_vencimento date NOT NULL,
    valor decimal(10,2),
    status_pagamento varchar(10) DEFAULT 'Pendente',
    id_residencia integer,
    
    CONSTRAINT FK_Taxa_Residencia 
        FOREIGN KEY(id_residencia) REFERENCES RESIDENCIA(id_residencia)
);

CREATE TABLE MULTA (
    id_multa INTEGER AUTO_INCREMENT PRIMARY KEY,
    data_emissao date NOT NULL,
    status_pagamento varchar(10) DEFAULT 'Pendente',
    valor DECIMAL(10, 2),
    descricao VARCHAR(220),
    id_residencia integer,

    CONSTRAINT FK_Multa_Residencia 
        FOREIGN KEY(id_residencia) REFERENCES RESIDENCIA(id_residencia)
);

CREATE TABLE AVISO (
    id_aviso INTEGER AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(50),
    texto VARCHAR(220),
    data_aviso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_administrador integer,
    condominio_cnpj varchar(16),

    CONSTRAINT FK_aviso_administrador
        FOREIGN KEY(id_administrador) REFERENCES ADMINISTRADOR(id_administrador),
    
    CONSTRAINT FK_aviso_condominio
        FOREIGN KEY(condominio_cnpj) REFERENCES CONDOMINIO(cnpj)
);

CREATE TABLE AREA_COMUM (
    id_area_comum INTEGER PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    capacidade INT,
    condominio_cnpj VARCHAR(16) NOT NULL,
    
    CONSTRAINT FK_area_comum_condominio 
        FOREIGN KEY (condominio_cnpj) REFERENCES CONDOMINIO(cnpj)
);