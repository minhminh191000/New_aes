from math import tan
from libary_aes import aes
from BitVector import *


class AES_encrypt():
    class Meta:
        ''' AES đang sử dụng là AES 128 với Khóa 128 , 192 , 254
            Yêu cầu sử dụng thì phải ghi rõ nguồn nhé :(
            Người viết tool : Minh - (Migor) '''
    def file_encrypt(file_XauRo,file_XauMa,KeyCharacter,Key):
        f = open(file_XauRo,mode = 'r',encoding = 'utf-8')
        KeyCharacter = aes.no_accent_vietnamese(KeyCharacter)
        data = f.readlines()
        PlainVersion =[]
        for i in range(len(data)):
            text = data[i]
            text = text.strip('\n')
            PlainVersion.append(text)
        wf = open(file_XauMa,mode = 'w',encoding = 'utf-8') 
        for i in range(len(PlainVersion)):
            if len(PlainVersion[i]) > 16:
                for j in range(0,len(PlainVersion[i]),16):
                    data = AES_encrypt.encrypt(PlainVersion[i][j:j+16],KeyCharacter,Key)
                    wf.write(data)
                wf.write("\n")
            else: 
                data = AES_encrypt.encrypt(PlainVersion[i],KeyCharacter,Key)
                wf.write(data)
                wf.write("\n")
        wf.close()
        return "data encrypt done"
            
        

    def encrypt(PlainVersion,KeyCharacter,Key):
        print("Mã hóa thông tin aes - Minh - (Migor)")
        try :
            if Key == "128":
                loop = 10
                key_text = 16
                text = aes.edit_text(KeyCharacter,key_text)
            elif Key == "192":
                loop = 12
                key_text = 24
                text = aes.edit_text(KeyCharacter,key_text)
            elif Key == "256":
                loop = 14
                key_text = 32
                text = aes.edit_text(KeyCharacter,key_text)
            else:
                return "Not Key" 
        except:
            return "Key Not Found"  
        data = text
        # print(text)
        roundkeys = []
        roundkey = aes.findroundkey(data,0)
        roundkeys.append(roundkey)
        for i in range(loop - 1):
            roundkey = aes.findroundkey(roundkeys[i],i+1)
            roundkeys.append(roundkey)
        # print(roundkeys)
        # print("=========== đã vào đến đây===========")
        # print(KeyCharacter)
        bv1 = BitVector(hexstring=text)
        bv2 = BitVector(textstring=PlainVersion)
        PlainVersion = bv1 ^ bv2
        PlainVersion = PlainVersion.get_bitvector_in_hex()
        # print("=========== đã vào đến đây===========")

        for i in range(loop-1):
            # thực hiện lặp Nr -1 lần
            # print('thực hiện mã hóa lần %d ' %(i+1))
            # subbyte
            subbyte = aes.subbyte(PlainVersion)
            # print(subbyte)
            # shifrow
            shifrow = aes.shiftrow(subbyte)
            # print(shifrow)
            # mixcolumn
            # print("=========== đã vào đến đây===========")
            mixcolumn =aes.mixcolumns(shifrow)
            # print("=========== đã vào đến đây===========")
            # addroundkey
            data1 = BitVector(hexstring=mixcolumn)
            data2 = BitVector(hexstring=roundkeys[i])
            addroundkey = aes.addroundkey(data1,data2)
            PlainVersion = addroundkey
            # print(PlainVersion)
            # thực hiện lặp Nr -1 lần
        # thực hiện lặp lần Nr
        # print('thực hiện mã hóa lần %d' %(loop))
        # subbyte
        subbyte = aes.subbyte(PlainVersion)
        # shifrow
        shifrow = aes.shiftrow(subbyte)
        # addroundkey
        data1 = BitVector(hexstring=shifrow)
        data2 = BitVector(hexstring=roundkeys[loop-1])
        addroundkey = aes.addroundkey(data1,data2)
        result =  addroundkey
        # thực hiện lặp lần Nr
        return  result

