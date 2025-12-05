
-- Criar tabelas
CREATE TABLE associado (
    id          INT IDENTITY(1,1) PRIMARY KEY,
    nome        VARCHAR(100),
    sobrenome   VARCHAR(100),
    idade       INT,
    email       VARCHAR(255)
);

CREATE TABLE conta (
    id            INT IDENTITY(1,1) PRIMARY KEY,
    tipo          VARCHAR(20),
    data_criacao  DATETIME2,
    id_associado  INT,
    FOREIGN KEY (id_associado) REFERENCES associado(id)
);

CREATE TABLE cartao (
    id            INT IDENTITY(1,1) PRIMARY KEY,
    num_cartao    BIGINT,
    nom_impresso  VARCHAR(100),
    id_conta      INT,
    id_associado  INT,
    FOREIGN KEY (id_conta) REFERENCES conta(id),
    FOREIGN KEY (id_associado) REFERENCES associado(id)
);

CREATE TABLE movimento (
    id              INT IDENTITY(1,1) PRIMARY KEY,
    vlr_transacao   DECIMAL(10,2),
    des_transacao   VARCHAR(255),
    data_movimento  DATETIME2,
    id_cartao       INT,
    FOREIGN KEY (id_cartao) REFERENCES cartao(id)
);
GO