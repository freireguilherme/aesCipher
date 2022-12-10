from Cryptodome.Cipher import AES
from hashlib import md5
from os import urandom
import argparse

def chave_derivada_e_vi(senha, tempero, k_lenght, vi_lenth):
    '''
    Essa função recebe a chave, salt, tamanho da chave e o tamnho
    de um vetor de inicialização que AES CBC precisa.

    Será usada pelas funções de encrypt e decrypt

    Retorna a senha em hash e o vetor de inicialização
    '''
    d = d_i = b'' #aqui a variavel d (e d_i) é uma sequencia de bytes
    while len(d) < k_lenght + vi_lenth: #k_length = 32 (default) + vi_length = 16 entao, total = 48bits
        d_i = md5(d_i + str.encode(senha) + tempero).digest() #obtive o valor hash da senha com o tempero
        d += d_i
    return d[:k_lenght], d[k_lenght:k_lenght + vi_lenth] #retorna a senha e o vetor de inicialização de 16bytes

def encrypt(arquivo_entrada, arquivo_saida, senha, k_length=32):
    '''
    função que encripta um arquivo.

    recebe um arquivo a ser encriptado, qual o nome do arquivo de saida, a chave e o tamnho da chave
    (padrão de 32bits)

    gera na saida um arquivo encriptado em AES 
    '''
    tb = AES.block_size #tamnho do bloco, 16bytes
    tempero = urandom(tb) #salt, string de tamnho tb de bytes random
    chave, vi = chave_derivada_e_vi(senha, tempero, k_length, tb) #chave em valor hash e vetor de inicialização
    cifra = AES.new(chave, AES.MODE_CBC, vi) #cifra em modo CBC
    arquivo_saida.write(tempero)
    completo = False

    while not completo:
        bloco = arquivo_entrada.read(1024 * tb)
        if len(bloco) == 0 or len(bloco) % tb != 0: #se o bloco nao for 16bytes
            tam_padding = (tb - len(bloco) % tb) or tb
            bloco += str.encode(tam_padding *chr(tam_padding)) #completa
            completo =  True
        arquivo_saida.write(cifra.encrypt(bloco)) #escreve o arquivo cifrado

def decrypt(arquivo_entrada, arquivo_saida, senha, k_length=32):
    tb = AES.block_size #tamnho do bloco
    tempero = arquivo_entrada.read(tb) #pego o tempero do arquivo criptografado 
    chave, vi = chave_derivada_e_vi(senha, tempero, k_length, tb) #chave em valor hash e vetor de inicialização
    cifra = AES.new(chave, AES.MODE_CBC, vi)
    prox_bloco = ''
    completo = False

    while not completo:
        bloco, prox_bloco = prox_bloco, cifra.decrypt(arquivo_entrada.read(1024 * tb))
        if len (prox_bloco) == 0:
            tam_padding = bloco[-1]
            bloco = bloco[:-tam_padding]
            completo = True
        arquivo_saida.write(bytes(x for x in bloco))

def main():
    '''Por meio de argumentos, informa se é motivo de encriptar ou decifrar, o nome do arquivo de 
    texto em txt a ser manipulado e o nome do arquivo de texto txt onde será a saída
    
    Um exemplo de como passar os argumentos para encriptar usando AES:

    python -u aes.py --enc textoclaro.txt --out textocifrado.txt --key 12345
    
    Exemplo para decifrar

    python -u aes.py --dec textocifrado.txt --out textoclaro.txt --key 12345
    '''

    parser = argparse.ArgumentParser(
    prog="Cifra AES",
    description="recebe um arquivo qualquer e devolve um arquivo num formato qualquer definido pelo usuario. Se --enc, encripta. Se --dec, decifra. Uso: aes.py --enc textoclaro.* --out textocifrado.* --key senha_do_usuario para cifrar. aes.py --dec textocifrado.* --out textoclaro.*. O nome do arquivo nao importa",
    epilog = "Programa para encriptar ou decifrar por meio da cifra AES. As opcoes sao --enc, --dec, --out e --key ",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-e", "--enc", action="store", type=str, help="encripta texto")
    parser.add_argument("-d", "--dec", action="store", type=str, help="decripta texto")
    parser.add_argument("-o", "--out", action="store", type=str, help="arquivo de saída")
    parser.add_argument("-k", "--key", action="store", type=str, help="senha")
    
    args = parser.parse_args()
    try:
        if (args.enc):
            with open(args.enc, 'rb') as arquivo_entrada, open(args.out, 'wb') as arquivo_saida:
                encrypt(arquivo_entrada, arquivo_saida, args.key )

        elif(args.dec):
            with open(args.dec, 'rb') as arquivo_entrada, open(args.out, 'wb') as arquivo_saida:
                decrypt(arquivo_entrada, arquivo_saida, args.key )

        else:
            print('opcção inválida. tente -h ou --help')
    except UnicodeEncodeError as error:
        print(error)
        print("Nao foi possivel, talvez algum caractere no texto de entrada nao pôde ser interpretado.")
    except KeyError as error:
        print(error)
        print("Nao foi possivel, talvez algum caractere no texto de entrada nao pôde ser interpretado.")
    except FileNotFoundError as error:
        print(error)
        print("Arquivo de entrada nao localizado")
main()