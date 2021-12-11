from math import tan
from libary_aes import aes
from BitVector import *


class AES_decrypt:
    class Meta:
        ''' Giai mã AES-128 với các khóa 128,192,256'''
    def file_decrypt(file_XauMa,file_XauRo,KeyCharacter,Key):
        # if Key =="128":
        #     total_key = 32
        # elif Key =="192":
        #     total_key = 24*2
        # elif Key == "256":
        #     total_key = 32*2
        f = open(file_XauMa,mode = 'r',encoding = 'utf-8')
        KeyCharacter = aes.no_accent_vietnamese(KeyCharacter)
        data = f.readlines()
        PlainVersion =[]
        for i in range(len(data)):
            text = data[i]
            text = text.strip('\n')
            PlainVersion.append(text)
        # print(PlainVersion)
        wf = open(file_XauRo,mode = 'w',encoding = 'utf-8') 
        for i in range(len(PlainVersion)):

            if len(PlainVersion[i]) > 32:
                for j in range(0,len(PlainVersion[i]),32):
                    data = AES_decrypt.decrypt(PlainVersion[i][j:j+32],KeyCharacter,Key)
                    wf.write(data)
                wf.write("\n")
            else:
                data = AES_decrypt.decrypt(PlainVersion[i],KeyCharacter,Key)
                wf.write(data)
                wf.write("\n")
        wf.close()
        return "data encrypt done"

    def decrypt(PlainVersion,KeyCharacter,Key):
        print("Giai mã AES-128 - Minh - (Migor)")
        ''' chuyển sang là hex luôn
            key là lấy sẵn ở Mã hóa  '''
        try :
            if Key == "128":
                loop = 10
                key_text = 16
                Nk = 4
                text = aes.edit_text(KeyCharacter,key_text)
            elif Key == "192":
                loop = 12
                key_text = 24
                Nk = 6
                text = aes.edit_text(KeyCharacter,key_text)
            elif Key == "256":
                loop = 14
                key_text = 32
                Nk = 8
                text = aes.edit_text(KeyCharacter,key_text)
            else:
                return "Not Key" 
        except:
            return "Key Not Found"  
        # print(text)
        data = text
        roundkeys = aes.KeyExpansion(data,Nk,loop)
        data1 = BitVector(hexstring=PlainVersion)
        data2 = BitVector(hexstring=roundkeys[loop])
        hex_addroundkey = aes.addroundkey(data1,data2)
        hex_shifrow = aes.inv_shifrow(hex_addroundkey)
        hex_subbyte = aes.inv_subbyte(hex_shifrow)

        for i in range(loop - 1,0,-1):
            data1 = BitVector(hexstring=hex_subbyte)
            data2 = BitVector(hexstring=roundkeys[i])
            hex_addroundkey = aes.addroundkey(data1,data2)
            hex_addroundkey = BitVector(hexstring=hex_addroundkey)
            hex_mixcolumn = aes.invmixcolumn(hex_addroundkey)
            hex_shifrow = aes.inv_shifrow(hex_mixcolumn)
            hex_subbyte =aes.inv_subbyte(hex_shifrow)
        # addroundkey phần đầu tiên
        data1 = BitVector(hexstring=hex_subbyte)
        data2 = BitVector(hexstring=roundkeys[0])
        hex_addroundkey = aes.addroundkey(data1,data2)
        output = aes.inv_formatText(hex_addroundkey)
        hex_to_ascii = ''
        for i in range(0,len(output),2):
            if output[i:i+2] == "00":
                pass
            else:
                hex_to_ascii = hex_to_ascii + output[i:i+2]
        PlainVersion = BitVector(hexstring=hex_to_ascii)
        PlainVersion = PlainVersion.get_bitvector_in_ascii()
        return PlainVersion



        