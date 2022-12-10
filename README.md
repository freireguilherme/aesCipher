### AES Cipher

Este é um pequeno programa que roda em terminal. Recebe como parâmetros um arquivo de entrada, o nome do arquivo de saída e uma chave.
Então este programa encripta ou decifra usando o algoritmo AES CBC e chave de 32bits.

### Utilização
Primeiro utilize o comando

`pip install pycryptodomex`

ou

`conda install pycryptodomex`

para instalar a lib de criptografia que contem o algoritmo AES.

Esse programa utiliza argumentos passados via terminal para realizar a tarefa desejada. Os argumentos são:
1. `--enc` : Se deseja encriptar em AES
2. `--dec` : Se deseja decifrar
3. `--out` : Nome do arquivo de saída
4. `--key` : Senha
   
No prompt de comando na pasta do arquivo aes.py, utilize o comando

`python -u aes.py --enc textoclaro.txt --out textocifrado.txt --key 12345`

para cifrar um arquivo. Note que o arquivo deve estar na mesma pasta que o programa aes.py. Note também que o tipo do arquivo de entrada pode ser qualquer um, desde que especificado. O nome e o tipo do arquivo de saída é de definição do usuário, assim como a senha a ser usada.

Para decifrar um arquivo criptografado em AES CBC, utilize o comando:

`python -u aes.py --dec textocifrado.txt --out textoclaro.txt --key 12345`

Se a senha for incorreta, o arquivo de saída continuará cifrado, mas nenhuma mensagem de erro é mostrada.

