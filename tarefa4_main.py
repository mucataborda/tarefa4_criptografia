import rsa
import os
from time import sleep
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import random


class Criptografador:
    def __init__(self, nome_usuario):
        while nome_usuario == '':
            print("Nome do usuário não pode ser vazio!")
            nome_usuario = str(input("Informe seu nome: "))
        self.nome_usuario = nome_usuario
        self.chave_pub = ''
        self.chave_priv = ''
        self.chave_sim = ''
        self.nome_arquivo = ''
        self.caminho_arq = ''
        self.iv = ''

    def get_nome_usuario(self):
        return self.nome_usuario

    def set_nome_arquivo(self, nome_arquivo):
        self.nome_arquivo = nome_arquivo

    def set_caminho_arq(self, caminho):
        self.caminho_arq = caminho

    def get_caminho_arq(self):
        return self.caminho_arq

    def gera_hash_random(self, tipo):
        hexa_string = '0123456789abcdef'
        chave_gerada = ''
        num_chaves = 1
        tamanho_chave = 0

        if tipo == 'k':
            tamanho_chave = 32
        elif tipo == 'iv':
            tamanho_chave = 16

        while(num_chaves != 0):
            chave_gerada = ''
            for n in range(0, tamanho_chave):
                random_position = random.randint(0, 15)
                chave_gerada += hexa_string[random_position]
            num_chaves -= 1

        return chave_gerada

    def gerar_chaves_assimetricas(self):
        print("\nGerando chaves assimetricas..")
        sleep(2)
        self.chave_pub, self.chave_priv = rsa.newkeys(2048)

    def gerar_chave_simetrica(self):
        print("\nGerando chave simetrica..")
        sleep(2)
        self.chave_sim = self.gera_hash_random('k')

    def gerar_iv(self):
        print("\nGerando vetor de inicialização..")
        sleep(2)
        self.iv = self.gera_hash_random('iv')

    def criptografar_mensagem(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        print("\nCriptografando mensagem...")
        sleep(2)

        def preenchimento(plaintext):
            return plaintext + b"\0" * (AES.block_size - len(plaintext) % AES.block_size)
        key = bytes(self.chave_sim, 'utf-8')
        IV = bytes(self.iv, 'utf-8')
        modo = AES.MODE_CBC
        gerador = AES.new(key, modo, IV=IV)
        texto = self.nome_arquivo
        texto = bytes(texto, 'utf-8')
        texto = preenchimento(texto)
        mensagem_criptografada = gerador.encrypt(texto)
        print("\nGerando arquivo..")
        sleep(2)
        arq = open((dir_path + '\Mensagem_criptografada.txt'), 'w')
        arq.write(str(mensagem_criptografada))
        arq.close()
        print("\nRemovendo arquivo em texto claro..")
        sleep(2)
        os.remove(self.get_caminho_arq())

    def criptografar_chave_e_iv(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        print("\nCriptografando chave simetrica e IV e salvando em arquivo..")

        chave_sim = self.chave_sim
        iv = self.iv
        encryption_chave_sim = rsa.encrypt(chave_sim.encode(), self.chave_pub)
        encryption_iv = rsa.encrypt(iv.encode(), self.chave_pub)

        print("Salvando chave..")
        sleep(1)
        arq = open((dir_path + '\chave_criptografada.txt'), 'w')
        arq.write(str(encryption_chave_sim))
        arq.close()

        print("Salvando IV..")
        sleep(1)
        arq = open((dir_path + '\iv_criptografado.txt'), 'w')
        arq.write(str(encryption_iv))
        arq.close()


def informar_nome_do_arquivo():
    texto = ''
    dir_path = os.path.dirname(os.path.realpath(__file__))
    nome_arquivo = str(
        input("\nInforme o nome do arquivo que deseja criptografar (ex: texto.txt): "))
    while nome_arquivo == '' or (nome_arquivo[-4]+nome_arquivo[-3]+nome_arquivo[-2]+nome_arquivo[-1]) not in '.txt':
        print(
            "\nNome do arquivo não pode ser vazio e extensão deve seguir o exemplo (.txt)!")
        nome_arquivo = str(
            input("\nInforme o nome do arquivo que deseja criptografar (ex: texto.txt): "))

    try:
        arquivo = dir_path + f'\{nome_arquivo}'
        arq = open(arquivo, 'r')
        nome_arquivo = arq.read()
        texto = nome_arquivo
        criptografia.set_caminho_arq(arquivo)

        return texto
    except FileNotFoundError:
        print("Arquivo não encontrado!")
        return texto


sistema_ativo = True
if __name__ == '__main__':
    while(sistema_ativo == True):
        print("\n|------------Sistema de Criptografia e Descriptografia------------|")
        print("selecione uma das opções abaixo: ")
        print("1) Criptografar Arquivo ....................()")
        print("2) Descriptografar Arquivo .................()")
        print("3) Sair ....................................()")

        escolha = int(input("Escolha uma das opções: "))

        if escolha == 1:
            nome_usuario = str(input("Informe seu nome: "))
            criptografia = Criptografador(nome_usuario)
            criptografia.gerar_chaves_assimetricas()
            arquivo = informar_nome_do_arquivo()
            while arquivo == '':
                print(
                    "Arquivo não encontrado ou não possui conteúdo para ser Criptografado!")
                arquivo = informar_nome_do_arquivo()
            criptografia.set_nome_arquivo(arquivo)
            cripto = input("Pressione ENTER para criptografar o arquivo")
            criptografia.gerar_chave_simetrica()
            criptografia.gerar_iv()
            criptografia.criptografar_mensagem()
            criptografia.criptografar_chave_e_iv()

            print(1)
        elif escolha == 2:
            print(2)
        else:
            print("\nSistema encerrado!")
            sistema_ativo = False
