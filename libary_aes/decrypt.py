from math import tan
from libary_aes import aes
from BitVector import *


class AES_decrypt:
    class Meta:
        ''' Giai mã AES-128 với các khóa 128,192,256'''
    def file_decrypt(file_XauMa,file_XauRo,KeyCharacter,Key):
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
            data = AES_decrypt.decrypt(PlainVersion[i],KeyCharacter,Key)
            wf.write(data)
            wf.write("\n")
        wf.close()
        return "data encrypt done"

    def decrypt(PlainVersion,KeyCharacter,Key):
        print("Giai mã AES-128 - Minh - (Migor)")
        # print(Key)
        
        ''' chuyển sang là hex luôn
            key là lấy sẵn ở Mã hóa  '''
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
        # print(text)
        data = text
        ''' Tạo khóa vòng khóa vòng phải giống với khóa ở bên mã hóa '''
        # data = aes.text_in_hex(text)
        roundkeys = []
        roundkey = aes.findroundkey(data,0)
        roundkeys.append(roundkey)
        for i in range(loop - 1):
            roundkey = aes.findroundkey(roundkeys[i],i+1)
            roundkeys.append(roundkey)
        # print(roundkeys)

        ''' Tạo khóa vòng khóa vòng phải giống với khóa ở bên mã hóa '''
        # addroundkey Vòng Nr
        # print("Giai mã %d" %(loop))
        data1 = BitVector(hexstring=PlainVersion)
        data2 = BitVector(hexstring=roundkeys[loop-1])
        # print(data1)
        # # data2 = roundkeys[loop-1]
        # print(data2)
        hex_addroundkey = aes.addroundkey(data1,data2)
        # print(hex_addroundkey)
        # print("addroundkey",hex_addroundkey)
       
        hex_shifrow = aes.inv_shifrow(hex_addroundkey)
        # print("shifrow",hex_shifrow)
    
        hex_subbyte = aes.inv_subbyte(hex_shifrow)
        # print("subbyte",hex_subbyte)

        for i in range(loop - 2,-1,-1):
            # print("Giai mã %d" %(i+1))
            # addroundkey
            data1 = BitVector(hexstring=hex_subbyte)
            data2 = BitVector(hexstring=roundkeys[i])
            hex_addroundkey = aes.addroundkey(data1,data2)
            # print(hex_addroundkey)
            # mixcolumn
            hex_addroundkey = BitVector(hexstring=hex_addroundkey)
            hex_mixcolumn = aes.invmixcolumn(hex_addroundkey)
            # print("mixcolumn",hex_mixcolumn)
            # shifrow
            hex_shifrow = aes.inv_shifrow(hex_mixcolumn)
            # print("shifrow",hex_shifrow)
            #
            hex_subbyte =aes.inv_subbyte(hex_shifrow)
            # print("subbyte",hex_subbyte)

           
            
        # addroundkey phần đầu tiên
        data1 = BitVector(hexstring=hex_subbyte)
        data2 = BitVector(hexstring=text)
        hex_addroundkey = aes.addroundkey(data1,data2)
        # print(hex_addroundkey)
        # data1 = BitVector(hexstring=hex_addroundkey)
        output = aes.inv_formatText(hex_addroundkey)
        New_output = output.strip('00')
        PlainVersion = BitVector(hexstring=New_output)
        PlainVersion = PlainVersion.get_bitvector_in_ascii()
        return PlainVersion



        