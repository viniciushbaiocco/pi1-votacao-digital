CREATE DATABASE projeto_integrador;
USE projeto_integrador;

CREATE TABLE eleitores ( 
	id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    titulo_eleitor CHAR(12) UNIQUE NOT NULL,
    cpf CHAR(12) UNIQUE NOT NULL,
    mesario BOOLEAN DEFAULT FALSE,
    chave_acesso CHAR(8) UNIQUE NOT NULL,
    status_votacao BOOLEAN DEFAULT FALSE NOT NULL
);

CREATE TABLE candidatos (
	id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    partido VARCHAR(50) NOT NULL,
    sigla_partido VARCHAR(6) NOT NULL,
    numero_votacao CHAR(2) UNIQUE NOT NULL
);

CREATE TABLE votos (
	id INT PRIMARY KEY AUTO_INCREMENT,
    id_candidato INT,
    data_hora DATETIME NOT NULL,
    protocolo_votacao VARCHAR(255) UNIQUE NOT NULL,
    FOREIGN KEY (id_candidato) REFERENCES candidatos(id)
);
