from BitVector import *
import math
import string
import re
# from re import UNICODE
def subbyte(hex_str):
    loop2 = 0
    data=""
    data2=""
    #        0      1     2      3    4      5    6     7     8     9     a    B      C     D     E     F
    Row0 = ['63', '7c', '77', '7b', 'f2', '6b', '6f', 'c5', '30', '01', '67', '2b', 'fe', 'd7', 'ab', '76'] #0
    Row1 = ['ca', '82', 'c9', '7d', 'fa', '59', '47', 'f0', 'ad', 'd4', 'a2', 'af', '9c', 'a4', '72', 'c0'] #1
    Row2 = ['b7', 'fd', '93', '26', '36', '3f', 'f7', 'cc', '34', 'a5', 'e5', 'f1', '71', 'd8', '31', '15'] #2
    Row3 = ['04', 'c7', '23', 'c3', '18', '96', '05', '9a', '07', '12', '80', 'e2', 'eb', '27', 'b2', '75'] #3
    Row4 = ['09', '83', '2c', '1a', '1b', '6e', '5a', 'a0', '52', '3b', 'd6', 'b3', '29', 'e3', '2f', '84'] #4
    Row5 = ['53', 'd1', '00', 'ed', '20', 'fc', 'b1', '5b', '6a', 'cb', 'be', '39', '4a', '4c', '58', 'cf'] #5
    Row6 = ['d0', 'ef', 'aa', 'fb', '43', '4d', '33', '85', '45', 'f9', '02', '7f', '50', '3c', '9f', 'a8'] #6
    Row7 = ['51', 'a3', '40', '8f', '92', '9d', '38', 'f5', 'bc', 'b6', 'da', '21', '10', 'ff', 'f3', 'd2'] #7
    Row8 = ['cd', '0c', '13', 'ec', '5f', '97', '44', '17', 'c4', 'a7', '7e', '3d', '64', '5d', '19', '73'] #8
    Row9 = ['60', '81', '4f', 'dc', '22', '2a', '90', '88', '46', 'ee', 'b8', '14', 'de', '5e', '0b', 'db'] #9
    Row10 = ['e0', '32', '3a', '0a', '49', '06', '24', '5c', 'c2', 'd3', 'ac', '62', '91', '95', 'e4', '79'] #A
    Row11 = ['e7', 'c8', '37', '6d', '8d', 'd5', '4e', 'a9', '6c', '56', 'f4', 'ea', '65', '7a', 'ae', '08'] #B
    Row12 = ['ba', '78', '25', '2e', '1c', 'a6', 'b4', 'c6', 'e8', 'dd', '74', '1f', '4b', 'bd', '8b', '8a'] #C
    Row13 = ['70', '3e', 'b5', '66', '48', '03', 'f6', '0e', '61', '35', '57', 'b9', '86', 'c1', '1d', '9e'] #D
    Row14 = ['e1', 'f8', '98', '11', '69', 'd9', '8e', '94', '9b', '1e', '87', 'e9', 'ce', '55', '28', 'df'] #E
    Row15 = ['8c', 'a1', '89', '0d', 'bf', 'e6', '42', '68', '41', '99', '2d', '0f', 'b0', '54', 'bb', '16'] #F


    x_box=[Row0,Row1,Row2,Row3,Row4,Row5,Row6,Row7,Row8,Row9,Row10,Row11,Row12,Row13,Row14,Row15]
    for loop in range(0, math.ceil(len(hex_str)/2) ):
        x = ""
        y = ""
        #convert character to integer
        x=int(hex_str[loop2],16)
        y=int(hex_str[loop2+1],16)
        data=x_box[x][y]
        loop2=loop2+2
        data2 = data2 + data
    return data2
#================== xor ===========================
def xor(x1,x2):
        x1=BitVector(hexstring=x1)
        x2=BitVector(hexstring=x2)
        x3=x1^x2
        return x3.get_bitvector_in_hex()
def mixcolumns(hex_str):
    data = BitVector(hexstring=hex_str)
    data01 = (data[0:8])
    data23 = (data[8:16])
    data45 = (data[16:24])
    data67 = (data[24:32])
    data89 = (data[32:40])
    data1011 = (data[40:48])
    data1213 = (data[48:56])
    data1415 = (data[56:64])
    data1617 = (data[64:72])
    data1819 = (data[72:80])
    data2021 = (data[80:88])
    data2223 = (data[88:96])
    data2425 = (data[96:104])
    data2627 = (data[104:112])
    data2829 = (data[112:120])
    data3031 = (data[120:128])

    eightlim = BitVector(bitstring='100011011')
    one = BitVector(bitstring='0001')
    two = BitVector(bitstring='0010')
    three = BitVector(bitstring='0011')

    temp_data1 = data01.gf_multiply_modular(two, eightlim, 8)
    temp_data2 = data23.gf_multiply_modular(three, eightlim, 8)
    new_data01 = temp_data1 ^ temp_data2 ^ data45 ^ data67

    temp_data2 = data23.gf_multiply_modular(two, eightlim, 8)
    temp_data3 = data45.gf_multiply_modular(three, eightlim, 8)
    new_data23 = data01 ^ temp_data2 ^ temp_data3 ^ data67

    temp_data3 = data45.gf_multiply_modular(two, eightlim, 8)
    temp_data4 = data67.gf_multiply_modular(three, eightlim, 8)
    new_data45 = data01 ^ data23 ^ temp_data3 ^ temp_data4

    temp_data1 = data01.gf_multiply_modular(three, eightlim, 8)
    temp_data4 = data67.gf_multiply_modular(two, eightlim, 8)
    new_data67 = temp_data1 ^ data23 ^ data45 ^ temp_data4

    temp_data1 = data89.gf_multiply_modular(two, eightlim, 8)
    temp_data2 = data1011.gf_multiply_modular(three, eightlim, 8)
    new_data89 = temp_data1 ^ temp_data2 ^ data1213 ^ data1415

    temp_data2 = data1011.gf_multiply_modular(two, eightlim, 8)
    temp_data3 = data1213.gf_multiply_modular(three, eightlim, 8)
    new_data1011 = data89 ^ temp_data2 ^ temp_data3 ^ data1415

    temp_data3 = data1213.gf_multiply_modular(two, eightlim, 8)
    temp_data4 = data1415.gf_multiply_modular(three, eightlim, 8)
    new_data1213 = data89 ^ data1011 ^ temp_data3 ^ temp_data4

    temp_data1 = data89.gf_multiply_modular(three, eightlim, 8)
    temp_data4 = data1415.gf_multiply_modular(two, eightlim, 8)
    new_data1415 = temp_data1 ^ data1011 ^ data1213 ^ temp_data4

    temp_data1 = data1617.gf_multiply_modular(two, eightlim, 8)
    temp_data2 = data1819.gf_multiply_modular(three, eightlim, 8)
    new_data1617 = temp_data1 ^ temp_data2 ^ data2021 ^ data2223

    temp_data2 = data1819.gf_multiply_modular(two, eightlim, 8)
    temp_data3 = data2021.gf_multiply_modular(three, eightlim, 8)
    new_data1819 = data1617 ^ temp_data2 ^ temp_data3 ^ data2223

    temp_data3 = data2021.gf_multiply_modular(two, eightlim, 8)
    temp_data4 = data2223.gf_multiply_modular(three, eightlim, 8)
    new_data2021 = data1617 ^ data1819 ^ temp_data3 ^ temp_data4

    temp_data1 = data1617.gf_multiply_modular(three, eightlim, 8)
    temp_data4 = data2223.gf_multiply_modular(two, eightlim, 8)
    new_data2223 = temp_data1 ^ data1819 ^ data2021 ^ temp_data4

    temp_data1 = data2425.gf_multiply_modular(two, eightlim, 8)
    temp_data2 = data2627.gf_multiply_modular(three, eightlim, 8)
    new_data2425 = temp_data1 ^ temp_data2 ^ data2829 ^ data3031

    temp_data2 = data2627.gf_multiply_modular(two, eightlim, 8)
    temp_data3 = data2829.gf_multiply_modular(three, eightlim, 8)
    new_data2627 = data2425 ^ temp_data2 ^ temp_data3 ^ data3031

    temp_data3 = data2829.gf_multiply_modular(two, eightlim, 8)
    temp_data4 = data3031.gf_multiply_modular(three, eightlim, 8)
    new_data2829 = data2425 ^ data2627 ^ temp_data3 ^ temp_data4

    temp_data1 = data2425.gf_multiply_modular(three, eightlim, 8)
    temp_data4 = data3031.gf_multiply_modular(two, eightlim, 8)
    new_data3031 = temp_data1 ^ data2627 ^ data2829 ^ temp_data4

    result_data = new_data01 + new_data23 + new_data45 + new_data67 + new_data89 + new_data1011 + new_data1213 + new_data1415 + new_data1617 + \
                new_data1819 + new_data2021 + new_data2223 + new_data2425 + new_data2627 + new_data2829 + new_data3031
    result_hex = result_data.get_bitvector_in_hex()
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


def addroundkey(data1,data2):
    result = data1 ^ data2
    return result.get_bitvector_in_hex()



''' Giai Mã ============================================================================'''


def inv_subbyte(hex_str):
    loop2 = 0
    data=""
    data2=""
    Row0 = ['52', '09', '6a', 'd5', '30', '36', 'a5', '38', 'bf', '40', 'a3', '9e', '81', 'f3', 'd7', 'fb']#0
    Row1 = ['7c', 'e3', '39', '82', '9b', '2f', 'ff', '87', '34', '8e', '43', '44', 'c4', 'de', 'e9', 'cb']#1
    Row2 = ['54', '7b', '94', '32', 'a6', 'c2', '23', '3d', 'ee', '4c', '95', '0b', '42', 'fa', 'c3', '4e']#2
    Row3 = ['08', '2e', 'a1', '66', '28', 'd9', '24', 'b2', '76', '5b', 'a2', '49', '6d', '8b', 'd1', '25']#3
    Row4 = ['72', 'f8', 'f6', '64', '86', '68', '98', '16', 'd4', 'a4', '5c', 'cc', '5d', '65', 'b6', '92']#4
    Row5 = ['6c', '70', '48', '50', 'fd', 'ed', 'b9', 'da', '5e', '15', '46', '57', 'a7', '8d', '9d', '84']#5
    Row6 = ['90', 'd8', 'ab', '00', '8c', 'bc', 'd3', '0a', 'f7', 'e4', '58', '05', 'b8', 'b3', '45', '06']#6
    Row7 = ['d0', '2c', '1e', '8f', 'ca', '3f', '0f', '02', 'c1', 'af', 'bd', '03', '01', '13', '8a', '6b']#7
    Row8 = ['3a', '91', '11', '41', '4f', '67', 'dc', 'ea', '97', 'f2', 'cf', 'ce', 'f0', 'b4', 'e6', '73']#8
    Row9 = ['96', 'ac', '74', '22', 'e7', 'ad', '35', '85', 'e2', 'f9', '37', 'e8', '1c', '75', 'df', '6e']#9
    Row10 = ['47', 'f1', '1a', '71', '1d', '29', 'c5', '89', '6f', 'b7', '62', '0e', 'aa', '18', 'be', '1b']#A
    Row11 = ['fc', '56', '3e', '4b', 'c6', 'd2', '79', '20', '9a', 'db', 'c0', 'fe', '78', 'cd', '5a', 'f4']#B
    Row12 = ['1f', 'dd', 'a8', '33', '88', '07', 'c7', '31', 'b1', '12', '10', '59', '27', '80', 'ec', '5f']#C
    Row13 = ['60', '51', '7f', 'a9', '19', 'b5', '4a', '0d', '2d', 'e5', '7a', '9f', '93', 'c9', '9c', 'ef']#D
    Row14 = ['a0', 'e0', '3b', '4d', 'ae', '2a', 'f5', 'b0', 'c8', 'eb', 'bb', '3c', '83', '53', '99', '61']#E
    Row15 = ['17', '2b', '04', '7e', 'ba', '77', 'd6', '26', 'e1', '69', '14', '63', '55', '21', '0c', '7d']#F


    inv_box=[Row0,Row1,Row2,Row3,Row4,Row5,Row6,Row7,Row8,Row9,Row10,Row11,Row12,Row13,Row14,Row15]
    for loop in range(0, math.ceil(len(hex_str)/2) ):
        x = ""
        y = ""
        #convert character to integer
        x=int(hex_str[loop2],16)
        y=int(hex_str[loop2+1],16)
        data=inv_box[x][y]
        loop2=loop2+2
        data2 = data2 + data
    return data2

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
def invmixcolumn(data):
        data01 = (data[0:8])
        data23 = (data[8:16])
        data45 = (data[16:24])
        data67 = (data[24:32])
        data89 = (data[32:40])
        data1011 = (data[40:48])
        data1213 = (data[48:56])
        data1415 = (data[56:64])
        data1617 = (data[64:72])
        data1819 = (data[72:80])
        data2021 = (data[80:88])
        data2223 = (data[88:96])
        data2425 = (data[96:104])
        data2627 = (data[104:112])
        data2829 = (data[112:120])
        data3031 = (data[120:128])

        eightlim = BitVector(bitstring='100011011')
        one = BitVector(bitstring='0001')
        two = BitVector(bitstring='0010')
        three = BitVector(bitstring='0011')
        nine = BitVector(bitstring='1001')
        eleven = BitVector(bitstring='1011')
        thirteen = BitVector(bitstring='1101')
        fourteen = BitVector(bitstring='1110')

        temp_data1 = data01.gf_multiply_modular(fourteen, eightlim, 8) #done
        temp_data2 = data23.gf_multiply_modular(eleven, eightlim, 8)
        temp_data3 = data45.gf_multiply_modular(thirteen, eightlim, 8)
        temp_data4 = data67.gf_multiply_modular(nine, eightlim, 8)
        new_data01 = temp_data1 ^ temp_data2 ^ temp_data3 ^ temp_data4

        temp_data1 = data01.gf_multiply_modular(nine, eightlim, 8) #done
        temp_data2 = data23.gf_multiply_modular(fourteen, eightlim, 8)
        temp_data3 = data45.gf_multiply_modular(eleven, eightlim, 8)
        temp_data4 = data67.gf_multiply_modular(thirteen, eightlim, 8)
        new_data23 = temp_data1 ^ temp_data2 ^ temp_data3 ^ temp_data4

        temp_data1 = data01.gf_multiply_modular(thirteen, eightlim, 8)#done
        temp_data2 = data23.gf_multiply_modular(nine, eightlim, 8)
        temp_data3 = data45.gf_multiply_modular(fourteen, eightlim, 8)
        temp_data4 = data67.gf_multiply_modular(eleven, eightlim, 8)
        new_data45 = temp_data1 ^ temp_data2 ^ temp_data3 ^ temp_data4

        temp_data1 = data01.gf_multiply_modular(eleven, eightlim, 8)#done
        temp_data2 = data23.gf_multiply_modular(thirteen, eightlim, 8)
        temp_data3 = data45.gf_multiply_modular(nine, eightlim, 8)
        temp_data4 = data67.gf_multiply_modular(fourteen, eightlim, 8)
        new_data67 = temp_data1 ^ temp_data2 ^ temp_data3 ^ temp_data4




        temp_data1 = data89.gf_multiply_modular(fourteen, eightlim, 8) #done
        temp_data2 = data1011.gf_multiply_modular(eleven, eightlim, 8)
        temp_data3 = data1213.gf_multiply_modular(thirteen, eightlim, 8)
        temp_data4 = data1415.gf_multiply_modular(nine, eightlim, 8)
        new_data89 = temp_data1 ^ temp_data2 ^ temp_data3 ^ temp_data4

        temp_data1 = data89.gf_multiply_modular(nine, eightlim, 8) #done
        temp_data2 = data1011.gf_multiply_modular(fourteen, eightlim, 8)
        temp_data3 = data1213.gf_multiply_modular(eleven, eightlim, 8)
        temp_data4 = data1415.gf_multiply_modular(thirteen, eightlim, 8)
        new_data1011 = temp_data1 ^ temp_data2 ^ temp_data3 ^ temp_data4

        temp_data1 = data89.gf_multiply_modular(thirteen, eightlim, 8)#done
        temp_data2 = data1011.gf_multiply_modular(nine, eightlim, 8)
        temp_data3 = data1213.gf_multiply_modular(fourteen, eightlim, 8)
        temp_data4 = data1415.gf_multiply_modular(eleven, eightlim, 8)
        new_data1213 = temp_data1 ^ temp_data2 ^ temp_data3 ^ temp_data4

        temp_data1 = data89.gf_multiply_modular(eleven, eightlim, 8)#done
        temp_data2 = data1011.gf_multiply_modular(thirteen, eightlim, 8)
        temp_data3 = data1213.gf_multiply_modular(nine, eightlim, 8)
        temp_data4 = data1415.gf_multiply_modular(fourteen, eightlim, 8)
        new_data1415 = temp_data1 ^ temp_data2 ^ temp_data3 ^ temp_data4




        temp_data1 = data1617.gf_multiply_modular(fourteen, eightlim, 8) #done
        temp_data2 = data1819.gf_multiply_modular(eleven, eightlim, 8)
        temp_data3 = data2021.gf_multiply_modular(thirteen, eightlim, 8)
        temp_data4 = data2223.gf_multiply_modular(nine, eightlim, 8)
        new_data1617 = temp_data1 ^ temp_data2 ^ temp_data3 ^ temp_data4

        temp_data1 = data1617.gf_multiply_modular(nine, eightlim, 8) #done
        temp_data2 = data1819.gf_multiply_modular(fourteen, eightlim, 8)
        temp_data3 = data2021.gf_multiply_modular(eleven, eightlim, 8)
        temp_data4 = data2223.gf_multiply_modular(thirteen, eightlim, 8)
        new_data1819 = temp_data1 ^ temp_data2 ^ temp_data3 ^ temp_data4

        temp_data1 = data1617.gf_multiply_modular(thirteen, eightlim, 8)#done
        temp_data2 = data1819.gf_multiply_modular(nine, eightlim, 8)
        temp_data3 = data2021.gf_multiply_modular(fourteen, eightlim, 8)
        temp_data4 = data2223.gf_multiply_modular(eleven, eightlim, 8)
        new_data2021 = temp_data1 ^ temp_data2 ^ temp_data3 ^ temp_data4

        temp_data1 = data1617.gf_multiply_modular(eleven, eightlim, 8)#done
        temp_data2 = data1819.gf_multiply_modular(thirteen, eightlim, 8)
        temp_data3 = data2021.gf_multiply_modular(nine, eightlim, 8)
        temp_data4 = data2223.gf_multiply_modular(fourteen, eightlim, 8)
        new_data2223 = temp_data1 ^ temp_data2 ^ temp_data3 ^ temp_data4





        temp_data1 = data2425.gf_multiply_modular(fourteen, eightlim, 8) #done
        temp_data2 = data2627.gf_multiply_modular(eleven, eightlim, 8)
        temp_data3 = data2829.gf_multiply_modular(thirteen, eightlim, 8)
        temp_data4 = data3031.gf_multiply_modular(nine, eightlim, 8)
        new_data2425 = temp_data1 ^ temp_data2 ^ temp_data3 ^ temp_data4

        temp_data1 = data2425.gf_multiply_modular(nine, eightlim, 8) #done
        temp_data2 = data2627.gf_multiply_modular(fourteen, eightlim, 8)
        temp_data3 = data2829.gf_multiply_modular(eleven, eightlim, 8)
        temp_data4 = data3031.gf_multiply_modular(thirteen, eightlim, 8)
        new_data2627 = temp_data1 ^ temp_data2 ^ temp_data3 ^ temp_data4

        temp_data1 = data2425.gf_multiply_modular(thirteen, eightlim, 8)#done
        temp_data2 = data2627.gf_multiply_modular(nine, eightlim, 8)
        temp_data3 = data2829.gf_multiply_modular(fourteen, eightlim, 8)
        temp_data4 = data3031.gf_multiply_modular(eleven, eightlim, 8)
        new_data2829 = temp_data1 ^ temp_data2 ^ temp_data3 ^ temp_data4

        temp_data1 = data2425.gf_multiply_modular(eleven, eightlim, 8)#done
        temp_data2 = data2627.gf_multiply_modular(thirteen, eightlim, 8)
        temp_data3 = data2829.gf_multiply_modular(nine, eightlim, 8)
        temp_data4 = data3031.gf_multiply_modular(fourteen, eightlim, 8)
        new_data3031 = temp_data1 ^ temp_data2 ^ temp_data3 ^ temp_data4

        new_data = new_data01 + new_data23 + new_data45 + new_data67 + new_data89 + new_data1011 + new_data1213 + new_data1415 + new_data1617 + new_data1819 + new_data2021 + new_data2223 + new_data2425 + new_data2627 + new_data2829 + new_data3031
        new_dataashex = new_data.get_bitvector_in_hex()
        return new_dataashex



'''======================================='''

def KeyExpansion(CipherKey,Nk,Nr):
        r_con = ['01000000', '02000000', '04000000', '08000000', '10000000',
                 '20000000', '40000000', '80000000', '1b000000', '36000000',
                 '6c000000', 'd8000000', 'ab000000', '4d000000']
        max_word = (Nr + 1) * 4
        i = 0
        for w in range(Nk, max_word, 1):
            # Copy previous word
            Wn = w * 8  
            word = CipherKey[Wn - 8: Wn]
            # Schedule_core mỗi 1 row
            if w % Nk == 0:
                # Rotate word
                word = shiftrow(word)
                # sub bytes
                word = subbyte(word)
                # xor Rcon
                word = xor(word, r_con[i])
                # increase i
                i = i + 1
            elif Nk == 8 and w % Nk == 4:
                # Sub bytes mỗi 4 word khi sử dụng
                # 256-bit key.
                word = subbyte(word)

            # Word tương đương
            previous = CipherKey[(w - Nk) * 8: (w - Nk + 1) * 8]
            # Xor với word tương đương
            word = xor(word, previous)
            # Nối vào
            CipherKey = CipherKey + word
        return [CipherKey[32 * i: 32 * (i + 1)] for i in range(len(CipherKey) // 32)]
'''======================================= Hàm Hỗ trợ========================================='''
# hàm dùng để sử lý            
def edit_text(data,key):
    # print(data)
    if len(data) < key:
        ListData = key - len(data)
        # print("Khóa Không đủ sẽ thực hiện thêm 0 vào cuối ")
        data = text_in_hex(data)
        # print(data)
        for i in range(ListData):
            data = data + "00"
        # print(data)
        return data
    elif len(data) > key:
        # print("Khóa Thừa sẽ thực hiện cắt")
        data = data[:key]
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



'''
192 - 24 khos dau vao

00112233    44556677    88990011    22334455    66778899    00112233
00  44  77  00  44  77  00
11
22
33
w0 w1 w2 w3 w4 w5 ->g
w6 ->
round 1 = w0 -> w3
round 2 = w4 -> w7
0011223344556677889900122334455

'''