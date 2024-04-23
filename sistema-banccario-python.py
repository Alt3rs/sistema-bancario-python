import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, endereco, contas):
        self.endereco = endereco
        self.contas = []

    def realizar_trasacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, contas, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico 

    def sacar(self, valor):
        saldo = self.saldo
        if valor > saldo:
            print("\n***** Falha! Saldo insuficiente. *****")

        elif valor > 0:
            self._saldo -= valor
            print("\n$$$$$ Saque realizado com sucesso! $$$$$")
            return True

        else:
            print("\n***** Falha! Valor informado inválido. *****")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n$$$$$ Deposito realizado com sucesso! $$$$$")
            
        else:
            print("\n***** Falha! Valor informado inválido. *****")
            return False
        
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite = 500, limite_saques = 3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_sauqes = limite_saques
    
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n***** Falha! O valor do saque excede o limite. *****")

        elif excedeu_saques:
            print("\n***** Falha! Número máximo de saques excedido. *****")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """
    
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )

class Transacao(ABC):

    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def menu():
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

def filtrar_cliente(cpf,clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n***** Falha! Cliente não possui conta. *****")
        return
    
    # FIXME: Não permite cliente escolher a conta 
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o CPF do clinete: ")
    cliente = filtrar_cliente(cpf, cliente)

    if not cliente:
        print("***** Falha! Cliente não encontrado. *****")
        return
    
    valor = float(input("Informe o valor do deposito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def sacar():
    cpf = input("Informe o CPF do clinete: ")
    cliente = filtrar_cliente(cpf, cliente)

    if not cliente:
        print("***** Falha! Cliente não encontrado. *****")
        return
    
    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do clinete: ")
    cliente = filtrar_cliente(cpf, cliente)

    if not cliente:
        print("***** Falha! Cliente não encontrado. *****")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

def criar_cliente(clientes): 
    cpf = input("Informe o CPF do (somente número): ")
    cliente = filtrar_cliente(cpf, cliente)

    if cliente:
        print("***** Falha! Já existe cliente com esse CPF. *****")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (formato dd-mm-aaaa):")
    endereco = input("Informe o endereço (formato logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome= nome, data_nascimento= data_nascimento, endereco= endereco)

    clientes.append(cliente)

    print("\n$$$$$ Cliente criado com sucesso! $$$$$")
    
def criar_conta(numero_conta, contas):
    cpf = input("Informe o CPF do clinete: ")
    cliente = filtrar_cliente(cpf, cliente)

    if not cliente:
        print("\n***** Falha! Usuário não encontrado, criação de conta encerrado. *****")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n$$$$$ Conta criada com sucesso! $$$$$")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\n***** Falha! Por favor selecione novamente a operação desejada. *****")

main()
