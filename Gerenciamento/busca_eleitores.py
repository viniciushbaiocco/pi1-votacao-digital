# entrada: CPF ou Título eleitor
# processamento: busca no banco de dados a correspondencia de inputs.
# o cpf está cifrado no banco, logo o input precisa passar pela cifragem para encontrar a correspondencia no banco
# exibe: nome eleitor, titualo eleitor, se mesário, se votou

from Menu import gerenciador_de_entrada as ge
from Menu import sub_menus as sb
import conexao_banco as conexao

cursor = conexao.cursor()


def busca_eleitor():
    print("\n--- Busca de eleitores ---")
    print("\nOpção 1: Busca pelo CPF")
    print("\nOpção 2: Busca pelo Título de eleitor")
    print("\nVoltar")

    opcao = ge.obter_entrada_inteira_valida("Digite uma opção: ", 1, 3)
    if opcao == 1:
        # no banco, cpf é CHAR(11)
        cpf = str(input("Digite o número do CPF a ser consultado: "))
        # validar o cpf digitado
        # criptografar o cpf digitado
        comando = cursor.execute(
            "SELECT nome, mesario, titulo_eleitor FROM cadastro_eleitores WHERE cpf = %s")
        cursor.execute(comando, (cpf,))
        dados_eleitor = cursor.fetchone()

    if opcao == 2:
        # preciso entender se input será str ou int
        titulo_eleitor = int(
            input("Digite o número do Título de eleitor a ser consultado: "))
        # validar o  digitado
        comando = cursor.execute(
            "SELECT nome, mesario, titulo_eleitor FROM cadastro_eleitores WHERE cpf = %s")
        cursor.execute(comando, (cpf,))
        dados_eleitor = cursor.fetchone()

    else:
        sb.exibir_menu_eleitores

    cursor.close()
    conexao.close()

    return dados_eleitor

    # fazer a busca dos inputs com seus correspondentes no banco de dados
    # retonar com nome eleitor
