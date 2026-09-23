Cópia pessoal do Projeto Integrador I da PUC-Campinas, desenvolvido originalmente em equipe de seis pessoas.

Minhas contribuições no projeto original: módulo completo de candidatos, listagem e remoção de eleitores, personalização da interface de terminal (biblioteca Rich), otimização e refatoração do código.

Uso este repositório para continuar desenvolvendo por conta própria.

# Sistema de Votação Digital

Back-end de um sistema de votação digital operado por terminal, desenvolvido como Projeto Integrador I do curso de Engenharia de Software da PUC-Campinas.

O sistema simula o ciclo completo de uma urna eletrônica: cadastro de eleitores e candidatos, emissão da zerésima, abertura da urna sob autenticação de mesário, votação com verificação de duplicidade, encerramento e emissão do boletim de urna. O foco do projeto é **segurança da informação** — validação matemática de documentos, criptografia de dados sensíveis e trilha de auditoria de todos os eventos.

## Tecnologias

- **Python 3** — linguagem principal
- **MySQL** — banco de dados relacional (`mysql-connector-python`)
- **Rich** e **pyfiglet** — interface e apresentação em terminal
- **python-dotenv** — isolamento de credenciais
- **Cifra de Hill** — criptografia implementada do zero (álgebra linear)

## Funcionalidades

**Cadastro e gerenciamento**
- Cadastro de eleitores e candidatos, com geração de chave de acesso
- Busca, listagem, edição e remoção de registros
- Recuperação de chave de acesso

**Votação**
- Autenticação de mesário para abertura e encerramento da urna
- Emissão da zerésima antes do início do pleito
- Registro de voto com verificação de eleitor já votante
- Emissão de protocolo de votação

**Resultados e auditoria**
- Boletim de urna
- Apuração de votos por partido
- Estatística de comparecimento
- Validação de integridade dos dados
- Log de ocorrências: abertura e encerramento de urna, voto computado, tentativa de voto duplo, acesso negado e protocolo emitido

## Estrutura do projeto

```
├── Cadastro/         # cadastro de eleitores, candidatos e chaves de acesso
├── Gerenciamento/    # busca, listagem, edição e remoção de registros
├── Menu/             # navegação e submenus da aplicação
├── Ocorrencias/      # registro de eventos para auditoria
├── Resultados/       # boletim de urna, apuração e validação de integridade
├── Validadores/      # validação de entrada e de documentos
├── Verificadores/    # consultas de existência e estado no banco
├── Visual/           # utilitários de apresentação no terminal
├── Votacao/          # abertura, voto, protocolo e encerramento
├── Zeresima/         # emissão da zerésima
├── criptografia/     # implementação da Cifra de Hill
├── database/         # conexão, script de criação e carga inicial
└── main.py           # ponto de entrada
```

A divisão em módulos por responsabilidade foi uma decisão deliberada: o projeto foi desenvolvido por seis pessoas em paralelo, e isolar cada área reduziu conflitos de integração e permitiu desenvolver e revisar cada parte separadamente.

A separação entre **Validadores** e **Verificadores** é intencional: validadores checam a entrada isoladamente (formato, dígitos verificadores, regras de preenchimento), enquanto verificadores consultam o banco para confirmar existência e estado — por exemplo, se um CPF já está cadastrado ou se aquele eleitor já votou.

## Decisões técnicas

**Validação matemática de documentos.** CPF e Título de Eleitor são validados pelo cálculo dos dígitos verificadores, incluindo os casos de sequência repetida e de resto menor que 2. Uma máscara correta não é suficiente para o cadastro: o documento precisa ser matematicamente válido.

**Cifra de Hill implementada do zero.** A criptografia usa uma matriz-chave 2×2 sobre um alfabeto de 36 símbolos (letras e dígitos, com Z=0). A implementação inclui MDC, algoritmo estendido de Euclides, inverso modular e inversão de matriz em aritmética modular, com verificação de que o determinante é invertível no módulo. O objetivo foi aplicar o algoritmo compreendendo sua matemática, e não invocar uma biblioteca pronta.

**Trilha de auditoria centralizada.** Cada tipo de ocorrência tem seu próprio log, e todos passam por uma função única de registro que padroniza o carimbo de tempo e o identificador de sessão. Isso substituiu a lógica de escrita que antes estava duplicada em cada módulo de ocorrência.

**Credenciais fora do repositório.** As configurações de acesso ao banco ficam em um `.env` local, versionado apenas como `.env.example`. O `.gitignore` cobre `.env`, `__pycache__/` e a pasta de armazenamento local.

## Como executar

**1. Dependências**

Python 3 e um servidor MySQL em execução.

```bash
pip install -r requirements.txt
```

**2. Banco de dados**

Crie um arquivo `.env` na raiz do projeto a partir do `.env.example` e preencha com as credenciais do seu MySQL. Em seguida, execute os scripts em `database/`:

```sql
-- no MySQL
source database/ScriptBanco.sql;
source database/InsercaoCandidatos.sql;
```

**3. Execução**

```bash
python main.py
```

Caso o comando não seja encontrado, use `python3 main.py`.

## Integrantes

Projeto acadêmico desenvolvido em equipe de seis integrantes:

- Arthur de Souza Gimenes Antiqueira
- Felipe Piva Silva
- Guilherme Luis da Silveira
- Leonardo Varela Vacari
- Rafael Jorge Nicolau Correia
- Vinícius Hegues Baiocco

Projeto Integrador I — Engenharia de Software, PUC-Campinas.
