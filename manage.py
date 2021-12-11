# https://the-x.cn/en-us/cryptography/Aes.aspx?fbclid=IwAR26B747wxLsWFhzvbgLFRcjIhlfAFe9JtA0fVTd8JIAsFFleRh9ul_BSDQ
from BitVector import *
from libary_aes.encrypt import AES_encrypt
from libary_aes.decrypt import AES_decrypt
# from libary_aes.decrypt import AES_decrypt

# code = input("Nhập ký tự khóa :")
# key = input("nhập mã khóa :")
code ="0123456789ABCDEF"
key ="192"
AES_encrypt.file_encrypt('libary_aes/XauRo.txt','libary_aes/XauMa.txt',code,key)
AES_decrypt.file_decrypt('libary_aes/XauMa.txt','libary_aes/XauRo1.txt',code,key)