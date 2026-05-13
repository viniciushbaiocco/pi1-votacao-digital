from database import conexao_banco as conect
from Validadores import confirmacao as conf, gerenciador_de_entrada as ge, validacao_cpf as val_cpf, validacao_titulo as val_tit
from criptografia import criptografia as crip
from colorama import Fore, Style

def remocao_eleitores():
    """
    A função exibe opções para receber valores str de cpf ou titulo de eleitor para remoção do eleitor no banco de dados.
    Utiliza de funções de criptografia, validação e gerenciamento de entrada.

    Args:
        none

    Returns:
        Exibe (print) os dados do eleitor a ser removido na tela para o usuário.
        Realiza a exclusão do eleitor no banco de dados após confirmação.
        Exibe opções de novas remoções ou troca de Menu.

    """


    conexao = conect.conexao_banco()
    cursor = conexao.cursor(dictionary=True)

    print(Fore.WHITE + Style.BRIGHT + "\n--- 3 - Excluir Eleitores ---")
    print(Fore.WHITE + Style.BRIGHT + "\nOpção 1: Remover pelo CPF")
    print(Fore.WHITE + Style.BRIGHT + "\nOpção 2: Remover pelo Título de eleitor")

    #enquanto a opção estiver fora do intervalo, continua pedindo um valor válido (min,max)
    opcao = ge.obter_entrada_inteira_valida("\nDigite uma opção: ", 1, 2)

    while opcao != 3:

        #MUDANÇA: inicializo eleitor=none no começo do loop para reaproveitar o mesmo bloco de exibição/confirmação fora do match (evita duplicar código nos dois cases)
        eleitor = None

        match opcao:
            case 1:
                #valida o CPF digitado
                cpf = str(input(Fore.WHITE + Style.BRIGHT + "\nDigite o número do CPF a ser removido: "))
                validacao_cpf = val_cpf.validacao_de_cpf(cpf)

                if validacao_cpf == True:
                    #criptografa o CPF digitado para comparar com o cifrado no banco
                    cpf_criptografado = crip.criptografar_cpf(cpf)
                    cursor.execute('SELECT * FROM eleitores WHERE cpf = %s', (cpf_criptografado,))
                    eleitor = cursor.fetchone()

                    #se eleitor não cadastrado, avisa o usuário
                    if eleitor is None:
                        print(Fore.YELLOW + Style.BRIGHT + "\nEleitor não cadastrado.")
                else:
                    print(Fore.YELLOW + Style.BRIGHT + "\nPor favor, refaça sua busca!")

            case 2:
                #valida o título de eleitor digitado
                titulo_eleitor = str(input(Fore.WHITE + Style.BRIGHT + "\nDigite o número do Título de Eleitor a ser removido: "))

                if val_tit.validar_titulo(titulo_eleitor):
                    cursor.execute('SELECT * FROM eleitores WHERE titulo_eleitor = %s', (titulo_eleitor,))
                    eleitor = cursor.fetchone()

                    #se eleitor não cadastrado, avisa o usuário
                    if eleitor is None:
                        print(Fore.YELLOW + Style.BRIGHT + "\nEleitor não cadastrado.")
                else:
                    print(Fore.WHITE + Style.BRIGHT + "\nTítulo de Eleitor inválido. Por favor, refaça sua busca!")


        #se eleitor encontrado, exibe os dados e confirma a remoção
        if eleitor is not None:

            #exibe os dados do eleitor
            print(Fore.WHITE + Style.BRIGHT + '=' * 50)
            print(Fore.WHITE + Style.BRIGHT + ' - Eleitor a ser removido - ')
            print(Fore.WHITE + Style.BRIGHT + '=' * 50)
            print(Fore.WHITE + Style.BRIGHT + f' ID: {eleitor['id']}')
            print(Fore.WHITE + Style.BRIGHT + f' Nome: {eleitor['nome']}')
            print(Fore.WHITE + Style.BRIGHT + f' CPF: {crip.descriptografar_cpf(eleitor["cpf"])}')
            print(Fore.WHITE + Style.BRIGHT + f' Título de Eleitor: {eleitor["titulo_eleitor"]}')
            if eleitor['mesario'] == 1:
                mesario = 'Sim'
            else:
                mesario = 'Não'
            if eleitor['status_votacao'] == 1:
                status_votacao = 'Já Votou'
            else:
                status_votacao = 'Não Votou'
            print(Fore.WHITE + Style.BRIGHT + f' Mesário: {mesario}')
            print(Fore.WHITE + Style.BRIGHT + f' Status de Votação: {status_votacao}')
            print(Fore.WHITE + Style.BRIGHT + '=' * 50)

            #MUDANÇA: passo extra de confirmação antes do DELETE para evitar exclusão acidental (não existe no busca_eleitores pq lá não tem operação destrutiva)
            print(Fore.WHITE + Style.BRIGHT + "\nDeseja realmente remover este eleitor? \n 1 - Sim \n 2 - Não")
            confirmacao = ge.obter_entrada_inteira_valida("Opção escolhida: ", 1, 2)

            if confirmacao == 1:
                cursor.execute('DELETE FROM eleitores WHERE id = %s', (eleitor['id'],))
                conexao.commit()
                print(Fore.WHITE + Style.BRIGHT + "\nEleitor removido com sucesso.")
                conf.confirmacao()
                break
            else:
                print(Fore.YELLOW + Style.BRIGHT + "\nRemoção cancelada pelo usuário.")
                conf.confirmacao()
                break

    cursor.close()
    conexao.close()