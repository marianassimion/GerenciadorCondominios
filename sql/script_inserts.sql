USE condominio;

-- 1. ADMINISTRADOR (5)
INSERT INTO ADMINISTRADOR (nome, email, senha) VALUES
('Carlos Silva', 'carlos@admin.com', '123'),
('Maria Souza', 'maria@admin.com', '123'),
('João Lima', 'joao@admin.com', '123'),
('Ana Costa', 'ana@admin.com', '123'),
('Pedro Rocha', 'pedro@admin.com', '123');

-- 2. CONDOMINIO (5)
INSERT INTO CONDOMINIO VALUES
('11111111000111', 1, 'Residencial Sol', 'Rua A', 'Centro', 'Brasília', 'DF', '70000-000'),
('22222222000122', 2, 'Residencial Lua', 'Rua B', 'Asa Sul', 'Brasília', 'DF', '70000-111'),
('33333333000133', 3, 'Residencial Estrela', 'Rua C', 'Asa Norte', 'Brasília', 'DF', '70000-222'),
('44444444000144', 4, 'Residencial Vida', 'Rua D', 'Taguatinga', 'Brasília', 'DF', '70000-333'),
('55555555000155', 5, 'Residencial Paz', 'Rua E', 'Ceilândia', 'Brasília', 'DF', '70000-444');


-- RESIDENCIA (5)
INSERT INTO RESIDENCIA (num_unidade, bloco, tipo, condominio_cnpj) VALUES
(101, 'A', 'Apartamento', '11111111000111'),
(202, 'B', 'Apartamento', '22222222000122'),
(303, 'C', 'Cobertura', '33333333000133'),
(404, 'D', 'Apartamento', '44444444000144'),
(505, 'E', 'Casa', '55555555000155');


-- MORADOR (5)
INSERT INTO MORADOR VALUES
('11111111111', 'Lucas Mendes', 'lucas@email.com', 1, TRUE),
('22222222222', 'Paula Ribeiro', 'paula@email.com', 2, FALSE),
('33333333333', 'Bruno Alves', 'bruno@email.com', 3, FALSE),
('44444444444', 'Fernanda Lima', 'fernanda@email.com', 4, FALSE),
('55555555555', 'Rafael Santos', 'rafael@email.com', 5, FALSE);

-- TELEFONE_MORADOR (5)
INSERT INTO TELEFONE_MORADOR (cpf_morador, numero) VALUES
('11111111111', '61999990001'),
('22222222222', '61999990002'),
('33333333333', '61999990003'),
('44444444444', '61999990004'),
('55555555555', '61999990005');


-- EMPREGADO (5)
INSERT INTO EMPREGADO VALUES
('66666666666', 'José Porteiro', 'Porteiro', 1001, '2022-01-01', 1800.00, '11111111000111', NULL),
('77777777777', 'Marcos Limpeza', 'Zelador', 1002, '2022-02-01', 2000.00, '22222222000122', NULL),
('88888888888', 'Ana Segurança', 'Segurança', 1003, '2022-03-01', 2200.00, '33333333000133', NULL),
('99999999999', 'Paulo Jardinagem', 'Jardineiro', 1004, '2022-04-01', 1900.00, '44444444000144', NULL),
('10101010101', 'Carla Recepção', 'Recepcionista', 1005, '2022-05-01', 2100.00, '55555555000155', NULL);


-- VEICULO (5)
INSERT INTO VEICULO VALUES
('ABC1234', 'Civic', 'Preto', '11111111111'),
('DEF5678', 'Gol', 'Branco', '22222222222'),
('GHI9012', 'Onix', 'Vermelho', '33333333333'),
('JKL3456', 'Corolla', 'Prata', '44444444444'),
('MNO7890', 'HB20', 'Azul', '55555555555');


-- TAXA (5)
INSERT INTO TAXA (data_emissao, data_vencimento, valor, status_pagamento, id_residencia) VALUES
('2024-01-01', '2024-01-10', 350.00, 'Pendente', 1),
('2024-01-01', '2024-01-10', 320.00, 'Pago', 2),
('2024-01-01', '2024-01-10', 400.00, 'Pendente', 3),
('2024-01-01', '2024-01-10', 360.00, 'Pago', 4),
('2024-01-01', '2024-01-10', 380.00, 'Pendente', 5);

-- MULTA (5)
INSERT INTO MULTA (data_emissao, data_vencimento, status_pagamento, valor, descricao, id_residencia) VALUES
('2024-02-01', '2024-02-10', 'Pendente', 150.00, 'Barulho excessivo', 1),
('2024-02-01', '2024-02-10', 'Pago', 200.00, 'Uso indevido da garagem', 2),
('2024-02-01', '2024-02-10', 'Pendente', 180.00, 'Lixo fora do horário', 3),
('2024-02-01', '2024-02-10', 'Pago', 220.00, 'Animal sem coleira', 4),
('2024-02-01', '2024-02-10', 'Pendente', 160.00, 'Obra sem autorização', 5);


-- AVISO (5)
INSERT INTO AVISO (titulo, texto, id_administrador, condominio_cnpj) VALUES
('Manutenção', 'Manutenção no elevador', 1, '11111111000111'),
('Reunião', 'Reunião de moradores', 2, '22222222000122'),
('Obras', 'Obra no estacionamento', 3, '33333333000133'),
('Piscina', 'Limpeza da piscina', 4, '44444444000144'),
('Segurança', 'Atualização da portaria', 5, '55555555000155');


-- ÁREA_COMUM (5)
INSERT INTO AREA_COMUM (nome, descricao, capacidade, condominio_cnpj) VALUES
('Piscina', 'Piscina adulto', 50, '11111111000111'),
('Salão de Festas', 'Eventos', 100, '22222222000122'),
('Churrasqueira', 'Área gourmet', 30, '33333333000133'),
('Academia', 'Espaço fitness', 40, '44444444000144'),
('Parquinho', 'Área infantil', 25, '55555555000155');
