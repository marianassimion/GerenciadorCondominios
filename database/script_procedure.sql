DROP PROCEDURE IF  EXISTS calcular_media_salario;
DROP PROCEDURE IF  EXISTS calcular_media_salario_por_condominio;
DELIMITER $$

CREATE PROCEDURE calcular_media_salario(
    OUT media_salario DECIMAL(10,2)
)
BEGIN
    SELECT AVG(salario) INTO media_salario
    FROM empregado;
END $$

DELIMITER ;
DELIMITER $$

CREATE PROCEDURE calcular_media_salario_por_condominio(
    IN p_cnpj VARCHAR(14),
    OUT media_salario DECIMAL(10,2)
)
BEGIN
    SELECT AVG(salario) INTO media_salario
    FROM empregado
    WHERE condominio_cnpj = p_cnpj;
END $$

DELIMITER ;

CALL calcular_media_salario_por_condominio(3, @media);
SELECT @media;

