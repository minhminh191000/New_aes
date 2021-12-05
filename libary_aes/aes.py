from BitVector import *
import math
import string
import re
# from re import UNICODE
def subbyte(myhexstring):
    loop2 = 0
    temp=""
    temp2=""
    #        0      1     2      3    4      5    6     7     8     9     a    B      C     D     E     F
    part0 = ['63', '7c', '77', '7b', 'f2', '6b', '6f', 'c5', '30', '01', '67', '2b', 'fe', 'd7', 'ab', '76'] #0
    part1 = ['ca', '82', 'c9', '7d', 'fa', '59', '47', 'f0', 'ad', 'd4', 'a2', 'af', '9c', 'a4', '72', 'c0'] #1
    part2 = ['b7', 'fd', '93', '26', '36', '3f', 'f7', 'cc', '34', 'a5', 'e5', 'f1', '71', 'd8', '31', '15'] #2
    part3 = ['04', 'c7', '23', 'c3', '18', '96', '05', '9a', '07', '12', '80', 'e2', 'eb', '27', 'b2', '75'] #3
    part4 = ['09', '83', '2c', '1a', '1b', '6e', '5a', 'a0', '52', '3b', 'd6', 'b3', '29', 'e3', '2f', '84'] #4
    part5 = ['53', 'd1', '00', 'ed', '20', 'fc', 'b1', '5b', '6a', 'cb', 'be', '39', '4a', '4c', '58', 'cf'] #5
    part6 = ['d0', 'ef', 'aa', 'fb', '43', '4d', '33', '85', '45', 'f9', '02', '7f', '50', '3c', '9f', 'a8'] #6
    part7 = ['51', 'a3', '40', '8f', '92', '9d', '38', 'f5', 'bc', 'b6', 'da', '21', '10', 'ff', 'f3', 'd2'] #7
    part8 = ['cd', '0c', '13', 'ec', '5f', '97', '44', '17', 'c4', 'a7', '7e', '3d', '64', '5d', '19', '73'] #8
    part9 = ['60', '81', '4f', 'dc', '22', '2a', '90', '88', '46', 'ee', 'b8', '14', 'de', '5e', '0b', 'db'] #9
    part10 = ['e0', '32', '3a', '0a', '49', '06', '24', '5c', 'c2', 'd3', 'ac', '62', '91', '95', 'e4', '79'] #A
    part11 = ['e7', 'c8', '37', '6d', '8d', 'd5', '4e', 'a9', '6c', '56', 'f4', 'ea', '65', '7a', 'ae', '08'] #B
    part12 = ['ba', '78', '25', '2e', '1c', 'a6', 'b4', 'c6', 'e8', 'dd', '74', '1f', '4b', 'bd', '8b', '8a'] #C
    part13 = ['70', '3e', 'b5', '66', '48', '03', 'f6', '0e', '61', '35', '57', 'b9', '86', 'c1', '1d', '9e'] #D
    part14 = ['e1', 'f8', '98', '11', '69', 'd9', '8e', '94', '9b', '1e', '87', 'e9', 'ce', '55', '28', 'df'] #E
    part15 = ['8c', 'a1', '89', '0d', 'bf', 'e6', '42', '68', '41', '99', '2d', '0f', 'b0', '54', 'bb', '16'] #F


    lookuptable=[part0,part1,part2,part3,part4,part5,part6,part7,part8,part9,part10,part11,part12,part13,part14,part15]
    for loop in range(0, math.ceil(len(myhexstring)/2) ):
        x = ""
        y = ""
        #convert character to integer
        x=int(myhexstring[loop2],16)
        y=int(myhexstring[loop2+1],16)
        temp=lookuptable[x][y]
        loop2=loop2+2
        temp2 = temp2 + temp
    return temp2
#================== xor ===========================
def xor(temp1,temp2):
        temp1=BitVector(hexstring=temp1)
        temp2=BitVector(hexstring=temp2)
        temp3=temp1^temp2
        return temp3.get_bitvector_in_hex()
def mixcolumns(hex_str):
    bv = BitVector(hexstring=hex_str)
    bv01 = (bv[0:8])
    bv23 = (bv[8:16])
    bv45 = (bv[16:24])
    bv67 = (bv[24:32])
    bv89 = (bv[32:40])
    bv1011 = (bv[40:48])
    bv1213 = (bv[48:56])
    bv1415 = (bv[56:64])
    bv1617 = (bv[64:72])
    bv1819 = (bv[72:80])
    bv2021 = (bv[80:88])
    bv2223 = (bv[88:96])
    bv2425 = (bv[96:104])
    bv2627 = (bv[104:112])
    bv2829 = (bv[112:120])
    bv3031 = (bv[120:128])

    eightlim = BitVector(bitstring='100011011')
    one = BitVector(bitstring='0001')
    two = BitVector(bitstring='0010')
    three = BitVector(bitstring='0011')

    tempbv1 = bv01.gf_multiply_modular(two, eightlim, 8)
    tempbv2 = bv23.gf_multiply_modular(three, eightlim, 8)
    newbv01 = tempbv1 ^ tempbv2 ^ bv45 ^ bv67

    tempbv2 = bv23.gf_multiply_modular(two, eightlim, 8)
    tempbv3 = bv45.gf_multiply_modular(three, eightlim, 8)
    newbv23 = bv01 ^ tempbv2 ^ tempbv3 ^ bv67

    tempbv3 = bv45.gf_multiply_modular(two, eightlim, 8)
    tempbv4 = bv67.gf_multiply_modular(three, eightlim, 8)
    newbv45 = bv01 ^ bv23 ^ tempbv3 ^ tempbv4

    tempbv1 = bv01.gf_multiply_modular(three, eightlim, 8)
    tempbv4 = bv67.gf_multiply_modular(two, eightlim, 8)
    newbv67 = tempbv1 ^ bv23 ^ bv45 ^ tempbv4

    tempbv1 = bv89.gf_multiply_modular(two, eightlim, 8)
    tempbv2 = bv1011.gf_multiply_modular(three, eightlim, 8)
    newbv89 = tempbv1 ^ tempbv2 ^ bv1213 ^ bv1415

    tempbv2 = bv1011.gf_multiply_modular(two, eightlim, 8)
    tempbv3 = bv1213.gf_multiply_modular(three, eightlim, 8)
    newbv1011 = bv89 ^ tempbv2 ^ tempbv3 ^ bv1415

    tempbv3 = bv1213.gf_multiply_modular(two, eightlim, 8)
    tempbv4 = bv1415.gf_multiply_modular(three, eightlim, 8)
    newbv1213 = bv89 ^ bv1011 ^ tempbv3 ^ tempbv4

    tempbv1 = bv89.gf_multiply_modular(three, eightlim, 8)
    tempbv4 = bv1415.gf_multiply_modular(two, eightlim, 8)
    newbv1415 = tempbv1 ^ bv1011 ^ bv1213 ^ tempbv4

    tempbv1 = bv1617.gf_multiply_modular(two, eightlim, 8)
    tempbv2 = bv1819.gf_multiply_modular(three, eightlim, 8)
    newbv1617 = tempbv1 ^ tempbv2 ^ bv2021 ^ bv2223

    tempbv2 = bv1819.gf_multiply_modular(two, eightlim, 8)
    tempbv3 = bv2021.gf_multiply_modular(three, eightlim, 8)
    newbv1819 = bv1617 ^ tempbv2 ^ tempbv3 ^ bv2223

    tempbv3 = bv2021.gf_multiply_modular(two, eightlim, 8)
    tempbv4 = bv2223.gf_multiply_modular(three, eightlim, 8)
    newbv2021 = bv1617 ^ bv1819 ^ tempbv3 ^ tempbv4

    tempbv1 = bv1617.gf_multiply_modular(three, eightlim, 8)
    tempbv4 = bv2223.gf_multiply_modular(two, eightlim, 8)
    newbv2223 = tempbv1 ^ bv1819 ^ bv2021 ^ tempbv4

    tempbv1 = bv2425.gf_multiply_modular(two, eightlim, 8)
    tempbv2 = bv2627.gf_multiply_modular(three, eightlim, 8)
    newbv2425 = tempbv1 ^ tempbv2 ^ bv2829 ^ bv3031

    tempbv2 = bv2627.gf_multiply_modular(two, eightlim, 8)
    tempbv3 = bv2829.gf_multiply_modular(three, eightlim, 8)
    newbv2627 = bv2425 ^ tempbv2 ^ tempbv3 ^ bv3031

    tempbv3 = bv2829.gf_multiply_modular(two, eightlim, 8)
    tempbv4 = bv3031.gf_multiply_modular(three, eightlim, 8)
    newbv2829 = bv2425 ^ bv2627 ^ tempbv3 ^ tempbv4

    tempbv1 = bv2425.gf_multiply_modular(three, eightlim, 8)
    tempbv4 = bv3031.gf_multiply_modular(two, eightlim, 8)
    newbv3031 = tempbv1 ^ bv2627 ^ bv2829 ^ tempbv4

    result_bv = newbv01 + newbv23 + newbv45 + newbv67 + newbv89 + newbv1011 + newbv1213 + newbv1415 + newbv1617 + \
                newbv1819 + newbv2021 + newbv2223 + newbv2425 + newbv2627 + newbv2829 + newbv3031
    result_hex = result_bv.get_bitvector_in_hex()
    return result_hex

        

#===================== shiftrow =========================
def shiftrow(str_hex):
    if(len(str_hex)==8):
        New_str_hex=str_hex[2]+str_hex[3]+str_hex[4]+str_hex[5]+str_hex[6]+str_hex[7]+str_hex[0]+str_hex[1]
        return New_str_hex
    else:
        New_str_hex_1  =  str_hex[0]  + str_hex[1]  + str_hex[10] + str_hex[11] + str_hex[20] + str_hex[21] + str_hex[30] + str_hex[31]
        New_str_hex_2  =  str_hex[8]  + str_hex[9]  + str_hex[18] + str_hex[19] + str_hex[28] + str_hex[29] + str_hex[6]  + str_hex[7]
        New_str_hex_3  =  str_hex[16] + str_hex[17] + str_hex[26] + str_hex[27] + str_hex[4]  + str_hex[5]  + str_hex[14] + str_hex[15] 
        New_str_hex_4  =  str_hex[24] + str_hex[25] + str_hex[2]  + str_hex[3]  + str_hex[12] + str_hex[13] + str_hex[22] + str_hex[23]
        New_str_hex =  New_str_hex_1 + New_str_hex_2 + New_str_hex_3 + New_str_hex_4
        return New_str_hex

    # 00112233 44556677 8899AABB CCDDEEFF 
    # 00 44 88 CC 
    # 11 55 99 DD 
    # 22 66 AA EE 
    # 33 77 BB FF 

    # 00112233 44556677 8899AABB CCDDEEFF
#=========================findroudkey=============================
def findroundkey(temp1,case):
    Rcon = ["01000000", '02000000','04000000','08000000','10000000','20000000',
            '40000000','80000000','1b000000','36000000','6C000000','D8000000','AB000000','4D000000']
    # if key == "128":
    w0=temp1[0:8]
    w1=temp1[8:16]
    w2=temp1[16:24]
    w3=temp1[24:32]
    temp2=temp1[24:32]
    temp2=shiftrow(temp2)
    temp2=subbyte(temp2)
    temp2=xor(temp2,Rcon[case])
    w4=xor(w0, temp2)
    w5=xor(w1, w4)
    w6=xor(w2, w5)
    w7=xor(w3, w6)
    temp3=w4+w5+w6+w7
    return temp3

def addroundkey(data1,data2):
    # print(data1)
    # print(data2)
    result = data1 ^ data2
    # print(result)
    return result.get_bitvector_in_hex()
''' Giai Mã ============================================================================'''


def inv_subbyte(myhexstring):
    loop2 = 0
    temp=""
    temp2=""
    part0 = ['52', '09', '6a', 'd5', '30', '36', 'a5', '38', 'bf', '40', 'a3', '9e', '81', 'f3', 'd7', 'fb']#0
    part1 = ['7c', 'e3', '39', '82', '9b', '2f', 'ff', '87', '34', '8e', '43', '44', 'c4', 'de', 'e9', 'cb']#1
    part2 = ['54', '7b', '94', '32', 'a6', 'c2', '23', '3d', 'ee', '4c', '95', '0b', '42', 'fa', 'c3', '4e']#2
    part3 = ['08', '2e', 'a1', '66', '28', 'd9', '24', 'b2', '76', '5b', 'a2', '49', '6d', '8b', 'd1', '25']#3
    part4 = ['72', 'f8', 'f6', '64', '86', '68', '98', '16', 'd4', 'a4', '5c', 'cc', '5d', '65', 'b6', '92']#4
    part5 = ['6c', '70', '48', '50', 'fd', 'ed', 'b9', 'da', '5e', '15', '46', '57', 'a7', '8d', '9d', '84']#5
    part6 = ['90', 'd8', 'ab', '00', '8c', 'bc', 'd3', '0a', 'f7', 'e4', '58', '05', 'b8', 'b3', '45', '06']#6
    part7 = ['d0', '2c', '1e', '8f', 'ca', '3f', '0f', '02', 'c1', 'af', 'bd', '03', '01', '13', '8a', '6b']#7
    part8 = ['3a', '91', '11', '41', '4f', '67', 'dc', 'ea', '97', 'f2', 'cf', 'ce', 'f0', 'b4', 'e6', '73']#8
    part9 = ['96', 'ac', '74', '22', 'e7', 'ad', '35', '85', 'e2', 'f9', '37', 'e8', '1c', '75', 'df', '6e']#9
    part10 = ['47', 'f1', '1a', '71', '1d', '29', 'c5', '89', '6f', 'b7', '62', '0e', 'aa', '18', 'be', '1b']#A
    part11 = ['fc', '56', '3e', '4b', 'c6', 'd2', '79', '20', '9a', 'db', 'c0', 'fe', '78', 'cd', '5a', 'f4']#B
    part12 = ['1f', 'dd', 'a8', '33', '88', '07', 'c7', '31', 'b1', '12', '10', '59', '27', '80', 'ec', '5f']#C
    part13 = ['60', '51', '7f', 'a9', '19', 'b5', '4a', '0d', '2d', 'e5', '7a', '9f', '93', 'c9', '9c', 'ef']#D
    part14 = ['a0', 'e0', '3b', '4d', 'ae', '2a', 'f5', 'b0', 'c8', 'eb', 'bb', '3c', '83', '53', '99', '61']#E
    part15 = ['17', '2b', '04', '7e', 'ba', '77', 'd6', '26', 'e1', '69', '14', '63', '55', '21', '0c', '7d']#F


    lookuptable=[part0,part1,part2,part3,part4,part5,part6,part7,part8,part9,part10,part11,part12,part13,part14,part15]
    for loop in range(0, math.ceil(len(myhexstring)/2) ):
        x = ""
        y = ""
        #convert character to integer
        x=int(myhexstring[loop2],16)
        y=int(myhexstring[loop2+1],16)
        temp=lookuptable[x][y]
        loop2=loop2+2
        temp2 = temp2 + temp
    return temp2

def inv_shifrow(hex_str):
    ''' ở phần mã hóa thì 8 bit đầu sẽ được dịch xuống cuối bây giờ mình sẽ làm ngược lại'''
    if len(hex_str) == 8:
        result = hex_str[6:8] + hex_str[0:2] + hex_str[2:4] + hex_str[4:6]
        return result
    else:
        # Dữ Nguyên
        result = hex_str[0:2] + hex_str[26:28] + hex_str[20:22] + hex_str[14:16]
        # Dịch 1
        result = result + hex_str[8:10] + hex_str[2:4] + hex_str[28:30] + hex_str[22:24]
        # Dịch 2 
        result = result + hex_str[16:18] + hex_str[10:12] + hex_str[4:6] + hex_str[30:32]
        # Dịch 3
        result = result + hex_str[24:26] + hex_str[18:20] + hex_str[12:14] + hex_str[6:8]
        return result
        # return invshiftrow(hex_str)
def invmixcolumn(bv3):
        bv01 = (bv3[0:8])
        bv23 = (bv3[8:16])
        bv45 = (bv3[16:24])
        bv67 = (bv3[24:32])
        bv89 = (bv3[32:40])
        bv1011 = (bv3[40:48])
        bv1213 = (bv3[48:56])
        bv1415 = (bv3[56:64])
        bv1617 = (bv3[64:72])
        bv1819 = (bv3[72:80])
        bv2021 = (bv3[80:88])
        bv2223 = (bv3[88:96])
        bv2425 = (bv3[96:104])
        bv2627 = (bv3[104:112])
        bv2829 = (bv3[112:120])
        bv3031 = (bv3[120:128])

        eightlim = BitVector(bitstring='100011011')
        one = BitVector(bitstring='0001')
        two = BitVector(bitstring='0010')
        three = BitVector(bitstring='0011')
        nine = BitVector(bitstring='1001')
        eleven = BitVector(bitstring='1011')
        thirteen = BitVector(bitstring='1101')
        fourteen = BitVector(bitstring='1110')

        tempbv1 = bv01.gf_multiply_modular(fourteen, eightlim, 8) #done
        tempbv2 = bv23.gf_multiply_modular(eleven, eightlim, 8)
        tempbv3 = bv45.gf_multiply_modular(thirteen, eightlim, 8)
        tempbv4 = bv67.gf_multiply_modular(nine, eightlim, 8)
        newbv01 = tempbv1 ^ tempbv2 ^ tempbv3 ^ tempbv4

        tempbv1 = bv01.gf_multiply_modular(nine, eightlim, 8) #done
        tempbv2 = bv23.gf_multiply_modular(fourteen, eightlim, 8)
        tempbv3 = bv45.gf_multiply_modular(eleven, eightlim, 8)
        tempbv4 = bv67.gf_multiply_modular(thirteen, eightlim, 8)
        newbv23 = tempbv1 ^ tempbv2 ^ tempbv3 ^ tempbv4

        tempbv1 = bv01.gf_multiply_modular(thirteen, eightlim, 8)#done
        tempbv2 = bv23.gf_multiply_modular(nine, eightlim, 8)
        tempbv3 = bv45.gf_multiply_modular(fourteen, eightlim, 8)
        tempbv4 = bv67.gf_multiply_modular(eleven, eightlim, 8)
        newbv45 = tempbv1 ^ tempbv2 ^ tempbv3 ^ tempbv4

        tempbv1 = bv01.gf_multiply_modular(eleven, eightlim, 8)#done
        tempbv2 = bv23.gf_multiply_modular(thirteen, eightlim, 8)
        tempbv3 = bv45.gf_multiply_modular(nine, eightlim, 8)
        tempbv4 = bv67.gf_multiply_modular(fourteen, eightlim, 8)
        newbv67 = tempbv1 ^ tempbv2 ^ tempbv3 ^ tempbv4




        tempbv1 = bv89.gf_multiply_modular(fourteen, eightlim, 8) #done
        tempbv2 = bv1011.gf_multiply_modular(eleven, eightlim, 8)
        tempbv3 = bv1213.gf_multiply_modular(thirteen, eightlim, 8)
        tempbv4 = bv1415.gf_multiply_modular(nine, eightlim, 8)
        newbv89 = tempbv1 ^ tempbv2 ^ tempbv3 ^ tempbv4

        tempbv1 = bv89.gf_multiply_modular(nine, eightlim, 8) #done
        tempbv2 = bv1011.gf_multiply_modular(fourteen, eightlim, 8)
        tempbv3 = bv1213.gf_multiply_modular(eleven, eightlim, 8)
        tempbv4 = bv1415.gf_multiply_modular(thirteen, eightlim, 8)
        newbv1011 = tempbv1 ^ tempbv2 ^ tempbv3 ^ tempbv4

        tempbv1 = bv89.gf_multiply_modular(thirteen, eightlim, 8)#done
        tempbv2 = bv1011.gf_multiply_modular(nine, eightlim, 8)
        tempbv3 = bv1213.gf_multiply_modular(fourteen, eightlim, 8)
        tempbv4 = bv1415.gf_multiply_modular(eleven, eightlim, 8)
        newbv1213 = tempbv1 ^ tempbv2 ^ tempbv3 ^ tempbv4

        tempbv1 = bv89.gf_multiply_modular(eleven, eightlim, 8)#done
        tempbv2 = bv1011.gf_multiply_modular(thirteen, eightlim, 8)
        tempbv3 = bv1213.gf_multiply_modular(nine, eightlim, 8)
        tempbv4 = bv1415.gf_multiply_modular(fourteen, eightlim, 8)
        newbv1415 = tempbv1 ^ tempbv2 ^ tempbv3 ^ tempbv4




        tempbv1 = bv1617.gf_multiply_modular(fourteen, eightlim, 8) #done
        tempbv2 = bv1819.gf_multiply_modular(eleven, eightlim, 8)
        tempbv3 = bv2021.gf_multiply_modular(thirteen, eightlim, 8)
        tempbv4 = bv2223.gf_multiply_modular(nine, eightlim, 8)
        newbv1617 = tempbv1 ^ tempbv2 ^ tempbv3 ^ tempbv4

        tempbv1 = bv1617.gf_multiply_modular(nine, eightlim, 8) #done
        tempbv2 = bv1819.gf_multiply_modular(fourteen, eightlim, 8)
        tempbv3 = bv2021.gf_multiply_modular(eleven, eightlim, 8)
        tempbv4 = bv2223.gf_multiply_modular(thirteen, eightlim, 8)
        newbv1819 = tempbv1 ^ tempbv2 ^ tempbv3 ^ tempbv4

        tempbv1 = bv1617.gf_multiply_modular(thirteen, eightlim, 8)#done
        tempbv2 = bv1819.gf_multiply_modular(nine, eightlim, 8)
        tempbv3 = bv2021.gf_multiply_modular(fourteen, eightlim, 8)
        tempbv4 = bv2223.gf_multiply_modular(eleven, eightlim, 8)
        newbv2021 = tempbv1 ^ tempbv2 ^ tempbv3 ^ tempbv4

        tempbv1 = bv1617.gf_multiply_modular(eleven, eightlim, 8)#done
        tempbv2 = bv1819.gf_multiply_modular(thirteen, eightlim, 8)
        tempbv3 = bv2021.gf_multiply_modular(nine, eightlim, 8)
        tempbv4 = bv2223.gf_multiply_modular(fourteen, eightlim, 8)
        newbv2223 = tempbv1 ^ tempbv2 ^ tempbv3 ^ tempbv4





        tempbv1 = bv2425.gf_multiply_modular(fourteen, eightlim, 8) #done
        tempbv2 = bv2627.gf_multiply_modular(eleven, eightlim, 8)
        tempbv3 = bv2829.gf_multiply_modular(thirteen, eightlim, 8)
        tempbv4 = bv3031.gf_multiply_modular(nine, eightlim, 8)
        newbv2425 = tempbv1 ^ tempbv2 ^ tempbv3 ^ tempbv4

        tempbv1 = bv2425.gf_multiply_modular(nine, eightlim, 8) #done
        tempbv2 = bv2627.gf_multiply_modular(fourteen, eightlim, 8)
        tempbv3 = bv2829.gf_multiply_modular(eleven, eightlim, 8)
        tempbv4 = bv3031.gf_multiply_modular(thirteen, eightlim, 8)
        newbv2627 = tempbv1 ^ tempbv2 ^ tempbv3 ^ tempbv4

        tempbv1 = bv2425.gf_multiply_modular(thirteen, eightlim, 8)#done
        tempbv2 = bv2627.gf_multiply_modular(nine, eightlim, 8)
        tempbv3 = bv2829.gf_multiply_modular(fourteen, eightlim, 8)
        tempbv4 = bv3031.gf_multiply_modular(eleven, eightlim, 8)
        newbv2829 = tempbv1 ^ tempbv2 ^ tempbv3 ^ tempbv4

        tempbv1 = bv2425.gf_multiply_modular(eleven, eightlim, 8)#done
        tempbv2 = bv2627.gf_multiply_modular(thirteen, eightlim, 8)
        tempbv3 = bv2829.gf_multiply_modular(nine, eightlim, 8)
        tempbv4 = bv3031.gf_multiply_modular(fourteen, eightlim, 8)
        newbv3031 = tempbv1 ^ tempbv2 ^ tempbv3 ^ tempbv4

        newbv = newbv01 + newbv23 + newbv45 + newbv67 + newbv89 + newbv1011 + newbv1213 + newbv1415 + newbv1617 + newbv1819 + newbv2021 + newbv2223 + newbv2425 + newbv2627 + newbv2829 + newbv3031
        newbvashex = newbv.get_bitvector_in_hex()
        return newbvashex




'''======================================= Hàm Hỗ trợ========================================='''
# hàm dùng để sử lý            
def edit_text(data,key):
    # print(data)
    if len(data) < 16:
        ListData = 16 - len(data)
        # print("Khóa Không đủ sẽ thực hiện thêm 0 vào cuối ")
        data = text_in_hex(data)
        # print(data)
        for i in range(ListData):
            data = data + "00"
        # print(data)
        return data
    elif len(data) > 16:
        # print("Khóa Thừa sẽ thực hiện cắt")
        data = data[:16]
        data = text_in_hex(data)
        return data
    data = text_in_hex(data)
    return data


def text_in_hex(data):
    NewData=BitVector(textstring=data)
    Text = NewData.get_bitvector_in_hex()
    return Text
def inv_formatText(hex_str: str):
    i = 0
    while i < len(hex_str):
        if hex_str[i:i + 2] == '0d':
            # if hex_str[i:i + 2] = 'OO'
            hex_str = hex_str[0:i] + hex_str[i + 2:len(hex_str)]
        else:
            i = i + 2

    # print(hex_str)
    return hex_str



def no_accent_vietnamese(s):
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(r'[Đ]', 'D', s)
    s = re.sub(r'[đ]', 'd', s)
    return s



            
# def expand_key(self, cipher_key):
#         r_con = ['01000000', '02000000', '04000000', '08000000', '10000000',
#                  '20000000', '40000000', '80000000', '1b000000', '36000000',
#                  '6c000000', 'd8000000', 'ab000000', '4d000000']
#         max_word = (self.rounds + 1) * 4
#         for n_w in range(self.cipher_word, max_word, 4):
#             n_bit = n_w * 8
#             # 1 word 8 bit hex
#             before = cipher_key[n_bit - 8: n_bit]

#             # Rotate word
#             before = self.shift_rows(before)

#             # sub bytes
#             before = self.sub_bytes(before)

#             # xor rcon
#             before = self.xor(before, r_con[math.ceil(n_w / 4) - 1])

#             for i in range(32, 0, -8):
#                 w = cipher_key[n_bit - i: n_bit - i + 8]
#                 w4 = self.xor(w, before)
#                 before = w4
#                 cipher_key = cipher_key + w4
#         round_key = []
#         for i in range(self.rounds + 1):
#             round_key.append(cipher_key[i * 32: (i + 1) * 32])
#         return round_key
