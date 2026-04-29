from abc import ABC, abstractmethod


class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        r = conta.sacar(self.valor)
        if r == True:
            conta.historico.adicionar_transacao(f'Saque de R${self.valor}')
        else:
            conta.historico.adicionar_transacao(f'Tentativa de saque de R${self.valor} - Saldo insuficiente')

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.depositar(self.valor)
        conta.historico.adicionar_transacao(f'Depósito de R${self.valor}')


class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)


class Cliente:
    def __init__(self, endereco, contas):
        self.endereco = endereco
        self.contas = contas
    

    def realizar_transacao(self, conta, transacao: Transacao):
        transacao.registrar(conta)


    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, endereco, contas, cpf, nome, data_nascimento):
        super().__init__(endereco, contas)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


class Conta:
    numero_conta = 1
    def __init__(self,
                 saldo,
                 agencia,
                 cliente,
                 historico):
        self._saldo = saldo
        self.numero = Conta.numero_conta
        Conta.numero_conta += 1
        self.agencia = agencia
        self.cliente = cliente
        self.historico = historico

    @property
    def saldo(self):
        return self._saldo
    
    def get_saldo(self):
        self.historico.adicionar_transacao('Consulta de saldo')
        return self._saldo
    
    @classmethod
    def nova_conta(cls, cliente):
        conta = cls(saldo=0, agencia='0001', cliente=cliente, historico=Historico())
        cliente.adicionar_conta(conta)
        print(f'Nova conta criada para {cliente.nome} com número da agencia: {conta.agencia} e o número da conta: {conta.numero}.')
        return conta

    def valor_disponivel(self):
        return self._saldo

    def sacar(self, valor):
        if valor <= 0:
            print('Valor de saque deve ser positivo.')
            return False
        if self.valor_disponivel() >= valor:
            self._saldo -= valor
            print(f'Saque de R${valor} realizado com sucesso.')
            return True
        else:
            print('Saldo insuficiente para realizar o saque.')
            return False

    def depositar(self, valor):
        self._saldo += valor
        print(f'Depósito de R${valor} realizado com sucesso.')
        return True


class ContaCorrente(Conta):
    def __init__(self,
                 saldo,
                 agencia,
                 cliente,
                 historico,
                 limite=500,
                 limite_saques=3):
        super().__init__(saldo, agencia, cliente, historico)
        self.limite = limite
        self.limite_saques = limite_saques

    def valor_disponivel(self):
        return self._saldo + self.limite
    
    def sacar(self, valor):
        if self.limite_saques <= 0:
            print('Limite de saques diários atingido.')
            return False
        sucesso = super().sacar(valor)

        if sucesso:
            self.limite_saques -= 1
        return sucesso
        

def main():
    contas = []

    while True:
        print('\n' + '='*40)
        print('Bem-vindo ao sistema bancário!')
        print('Escolha a opção desejada: ')
        print('1 - Criar nova conta')
        print('2 - Realizar saque')
        print('3 - Realizar depósito')
        print('4 - Consultar saldo')
        print('5 - Historico de transações')
        print('6 - Sair')
        opcao = input('Opção: ')

        if opcao == '1':
            print('='*20, 'Abertura de conta', '='*20)
            nome = input('Digite o nome do cliente: ')
            cpf = input('Digite o CPF do cliente: ')
            data_nascimento = input('Digite a data de nascimento do cliente (dd/mm/aaaa): ')
            endereco = input('Digite o endereço do cliente: ')
            cliente = PessoaFisica(endereco=endereco, contas=[], cpf=cpf, nome=nome, data_nascimento=data_nascimento)
            conta = ContaCorrente.nova_conta(cliente)
            contas.append(conta)

        elif opcao == '2':
            print('='*20, 'Saque', '='*20)
            numero_conta = int(input('Digite o número da conta para saque: '))
            valor = float(input('Digite o valor do saque: '))
            if numero_conta in [conta.numero for conta in contas]:
                conta = [conta for conta in contas if conta.numero == numero_conta][0]
                transacao = Saque(valor)
                cliente = conta.cliente
                cliente.realizar_transacao(conta, transacao)

        elif opcao == '3':
            print('='*20, 'Depósito', '='*20)
            numero_conta = int(input('Digite o número da conta para depósito: '))
            valor = float(input('Digite o valor do depósito: '))
            if numero_conta in [conta.numero for conta in contas]:
                conta = [conta for conta in contas if conta.numero == numero_conta][0]
                transacao = Deposito(valor)
                cliente = conta.cliente
                cliente.realizar_transacao(conta, transacao)

        elif opcao == '4':
            print('='*20, 'Consulta de Saldo', '='*20)
            numero_conta = int(input('Digite o número da conta para consulta de saldo: '))
            if numero_conta in [conta.numero for conta in contas]:
                conta = [conta for conta in contas if conta.numero == numero_conta][0]
                saldo = conta.get_saldo()
                print(f'Saldo disponível: R${saldo}')

        elif opcao == '5':
            print('='*20, 'Histórico de Transações', '='*20)
            numero_conta = int(input('Digite o número da conta para histórico de transações: '))
            if numero_conta in [conta.numero for conta in contas]:
                conta = [conta for conta in contas if conta.numero == numero_conta][0]
                print('Transações realizadas:')
                for transacao in conta.historico.transacoes:
                    print(transacao)
        
        elif opcao == '6':
            print('Obrigado por usar o sistema bancário. Até logo!')
            break


if __name__ == '__main__':
    main()
