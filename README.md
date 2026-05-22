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
    Bibliotecas Exigidas: Listadas em requirements: [requirements.txt](requirements.txt)
    Criptografia: Cifra de Hill (Álgebra Linear)

**Como Executar o Sistema**

**1.** Requisitos e Dependências Certifique-se de ter o Python 3 e o MySQL funcionando em sua máquina. Em seguida, instale as bibliotecas requisitadas executando no terminal:

    pip install -r requirements.txt

**2.** Preparando o Banco de Dados

    Crie um arquivo .env localmente dentro da pasta desse projeto.
    Copie o texto de env example.
    Mude as variáveis padrões para as suas, dentro do arquivo .env criado por você, que permitem acesso ao MySQL.
    Execute o script ScriptBanco.sql no seu MySQL para criar as tabelas.

**3.** Rodando a Aplicação Abra o terminal na pasta raiz do projeto e inicie o sistema executando:

    python main.py

Caso apareca command not found:

    python3 main.py
