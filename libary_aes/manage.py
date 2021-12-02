# https://the-x.cn/en-us/cryptography/Aes.aspx?fbclid=IwAR26B747wxLsWFhzvbgLFRcjIhlfAFe9JtA0fVTd8JIAsFFleRh9ul_BSDQ
import aes
from BitVector import *
from decrypt import AES_decrypt
from encrypt import AES_encrypt

# code = input("Nhập ký tự khóa :")
# key = input("nhập mã khóa :")
code ="Minh yệu ém"
key ="128"
AES_encrypt.file_encrypt('XauRo.txt','XauMa.txt',code,key)
AES_decrypt.file_decrypt('XauMa.txt','XauRo1.txt',code,key)