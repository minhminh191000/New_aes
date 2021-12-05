from datetime import datetime

from AESManager import AESManager
type = 128
key = "cuongdeptrai"
aes = AESManager(type)
start_time = datetime.now()
cipher_text = aes.encrypt(key, "cuongdeptrai")
print("Cipher text: %s" % cipher_text)
print("Time encrypt : ", datetime.now()-start_time)
aes = AESManager(type)
start_time = datetime.now()
plain_text = aes.decrypt(key, cipher_text)
print("Plain text: %s" % plain_text)
print("Time decrypt : ", datetime.now()-start_time)
