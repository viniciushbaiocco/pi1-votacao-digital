**- Sistema de Votação Digital -**

O projeto é o backend de um sistema de votação digital via terminal desenvolvido para fins educacionais. O projeto possui dois módulos principais (Gerenciamento e Votação) e tem como foco a segurança da informação. Para isso, implementa validação matemática de documentos (CPF e Título de Eleitor), sistema de logs para auditoria de eventos e proteção de dados sensíveis (como chaves de acesso e protocolos) utilizando a criptografia da Cifra de Hill.

**Integrantes**

    Arthur de Souza Gimenes Antiqueira 
    Felipe Piva Silva
    Guilherme Luis da Silveira 
    Leonardo Varela Vacari
    Rafael Jorge Nicolau Correia
    Vinícius Hegues Baiocco 

**Tecnologias Utilizadas**

    Linguagem: Python 3.x
    Banco de Dados: MySQL
    Bibliotecas Exigidas: mysql.connector e datetime
    Criptografia: Cifra de Hill (Álgebra Linear)

**Como Executar o Sistema**

**1.** Requisitos e Dependências Certifique-se de ter o Python 3 e o MySQL rodando na sua máquina. Em seguida, instale a biblioteca de conexão executando no terminal:

pip install mysql-connector-python

**2.** Preparando o Banco de Dados

    Execute o script ScriptBanco.sql no seu MySQL para criar as tabelas.
    Abra o código [] e preencha as variáveis com seu usuário e senha local do MySQL.

**3.** Rodando a Aplicação Abra o terminal na pasta raiz do projeto e inicie o sistema executando:

python []
