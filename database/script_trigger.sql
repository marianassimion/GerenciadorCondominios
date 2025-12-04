CREATE TRIGGER trg_log_alteracao_salario
BEFORE UPDATE ON EMPREGADO
FOR EACH ROW
BEGIN
    -- Só registra se o salário mudou
    IF NEW.salario <> OLD.salario THEN
        INSERT INTO LOG_ALTERACAO_SALARIO
            (cpf_empregado, salario_antigo, salario_novo)
        VALUES
            (OLD.cpf, OLD.salario, NEW.salario);
    END IF;
END $$