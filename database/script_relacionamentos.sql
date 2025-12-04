/* SISTEMA DE GERENCIAMENTO DE CONDOMINIOS */

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
    id_administrador INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL
);

CREATE TABLE CONDOMINIO (
    cnpj VARCHAR(14) PRIMARY KEY,
    id_admin INT UNSIGNED NOT NULL,
    nome VARCHAR(65) NOT NULL,
    logradouro VARCHAR(100) NOT NULL,
    bairro VARCHAR(50) NOT NULL,
    cidade VARCHAR(50) NOT NULL,
    uf CHAR(2) NOT NULL,
    cep VARCHAR(9) NOT NULL,

    CONSTRAINT FK_condominio_admin 
        FOREIGN KEY (id_admin) REFERENCES ADMINISTRADOR(id_administrador)
);

CREATE TABLE RESIDENCIA (
    id_residencia INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    num_unidade INT UNSIGNED NOT NULL, 
    bloco VARCHAR(10),
    tipo VARCHAR(50),
    condominio_cnpj VARCHAR(14),

    CONSTRAINT FK_residencia_condominio 
        FOREIGN KEY (condominio_cnpj) REFERENCES CONDOMINIO(cnpj)
);

CREATE TABLE MORADOR (
    cpf VARCHAR(11) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    id_residencia INT UNSIGNED NOT NULL,
    sindico BOOLEAN NOT NULL DEFAULT FALSE, 

    CONSTRAINT FK_morador_residencia 
        FOREIGN KEY (id_residencia) REFERENCES RESIDENCIA(id_residencia)
);

CREATE TABLE TELEFONE_MORADOR (
    id_telefone_morador INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    cpf_morador VARCHAR(11) NOT NULL,
    numero VARCHAR(11),

    CONSTRAINT FK_telefone_morador 
        FOREIGN KEY (cpf_morador) REFERENCES MORADOR(cpf) 
        ON DELETE CASCADE
);

CREATE TABLE EMPREGADO (
    cpf VARCHAR(11) PRIMARY KEY,
    nome VARCHAR(65) NOT NULL,
    cargo VARCHAR(150) NOT NULL,
    matricula INT UNSIGNED UNIQUE,
    data_admissao DATE NOT NULL,
    salario DECIMAL(10,2),
    foto VARCHAR(255),
    condominio_cnpj VARCHAR(14) NOT NULL,

    CONSTRAINT FK_empregado_condominio 
        FOREIGN KEY (condominio_cnpj) REFERENCES CONDOMINIO(cnpj)
);

CREATE TABLE VEICULO (
    placa VARCHAR(10) PRIMARY KEY,
    modelo VARCHAR(40) NOT NULL,
    cor VARCHAR(20),
    morador_cpf VARCHAR(11) NOT NULL,

    CONSTRAINT FK_veiculo_morador 
        FOREIGN KEY (morador_cpf) REFERENCES MORADOR(cpf)
);

CREATE TABLE TAXA (
    id_taxa INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    data_emissao DATE NOT NULL,
    data_vencimento DATE NOT NULL,
    valor DECIMAL(10,2),
    status_pagamento VARCHAR(10) DEFAULT 'Pendente',
    id_residencia INT UNSIGNED NOT NULL,

    CONSTRAINT FK_Taxa_Residencia 
        FOREIGN KEY (id_residencia) REFERENCES RESIDENCIA(id_residencia)
);

CREATE TABLE MULTA (
    id_multa INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    data_emissao DATE NOT NULL,
    data_vencimento DATE NOT NULL,
    status_pagamento VARCHAR(10) DEFAULT 'Pendente',
    valor DECIMAL(10,2),
    descricao VARCHAR(220),
    id_residencia INT UNSIGNED NOT NULL,

    CONSTRAINT FK_Multa_Residencia 
        FOREIGN KEY (id_residencia) REFERENCES RESIDENCIA(id_residencia)
);

CREATE TABLE AVISO (
    id_aviso INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(50),
    texto VARCHAR(220),
    data_aviso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_administrador INT UNSIGNED,
    condominio_cnpj VARCHAR(14) NOT NULL,

    CONSTRAINT FK_aviso_administrador
        FOREIGN KEY (id_administrador) REFERENCES ADMINISTRADOR(id_administrador),

    CONSTRAINT FK_aviso_condominio
        FOREIGN KEY (condominio_cnpj) REFERENCES CONDOMINIO(cnpj)
);

CREATE TABLE AREA_COMUM (
    id_area_comum INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    capacidade INT,
    condominio_cnpj VARCHAR(14) NOT NULL,

    CONSTRAINT FK_area_comum_condominio 
        FOREIGN KEY (condominio_cnpj) REFERENCES CONDOMINIO(cnpj)
);
