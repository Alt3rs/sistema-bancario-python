import textwrap

def menu ():
    menu = """
    =============== Menu =============== 
    [d] - Depositar
    [s] - Sacar
    [e] - Extrato
    [nc] - Nova Conta
    [lc] - Listar Contas
    [nu] - Novo Usuário
    [q] - Sair
    ====================================
    """
    return input(textwrap.dedent(menu))

def depositar (saldo, valor, extrato, / ):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
    else:
        print("Falha! Valor para depósito incorreto.") 

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor > saldo:
        print("Falha! Saldo insuficiente.")

    elif valor > limite:
        print("Falha! Valor excede o limite de saque")

    elif numero_saques >= limite_saques:
        print("Falha! Número de saques excedidos.")
            
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
            
    else:
        print("Falha! Valor informado incorreto.")

    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):   
    print("======================== Extrato ======================== ")      
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("========================================================= ")

def criar_usuario(usuarios):
    cpf = input("Informe  o CPF (informe somente o número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Falha! Já existe um usuário cadastrado com este CPF")
        return
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (informe no formato dd-mm-aaaa): ")
    endereco = input("Informe o endereço (informe no formato logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento,"cpf": cpf, "endereco" : endereco})

    print("Usuário criado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o cpf do usuário(informe somente o número):")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Conta criada com sucesso!")
        return {"agencia" : agencia, "numero_conta" : numero_conta, "usuario" : usuario}
    
    print("Falha! Usuário não encontrado, criação de conta encerrado")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência: \t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
    print("=" * 100)
    print(textwrap.dedent(linha))

    
def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0   
    usuarios = []
    contas = []
    
    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor a ser depositado: "))
            saldo, extrato = depositar(saldo, valor, extrato)
        
        elif opcao == "s":
            valor = float(input("Informe o valor a ser sacado: "))
            saldo, extrato = sacar(saldo = saldo, valor = valor, extrato = extrato, limite = limite, numero_saques = numero_saques, limite_saques = LIMITE_SAQUES,)
            
        elif opcao == "e":
           exibir_extrato(saldo, extrato= extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)
        
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
        
        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else: 
            print("Operação inválida, por favor selecione novamente a operação desejada.")
main()