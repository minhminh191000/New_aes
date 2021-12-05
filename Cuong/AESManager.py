from BitVector import BitVector
from utils import s_box_table, text_to_number, iv_s_box_table
import math


class AESManager:
    def __init__(self, style=128, debug=False):
        self.is_debug = debug
        if style == 128:
            self.rounds = 10
            self.cipher_word = 4
        elif style == 192:
            self.rounds = 12
            self.cipher_word = 6
        elif style == 256:
            self.rounds = 14
            self.cipher_word = 8
        else:
            raise Exception("Chi ma hoa AES-128, AES-192 va AES-256")
        self.round_keys = []
        return

    def debug(self, *args):
        if self.is_debug:
            print(*args)

    # def gen_round_keys(self, passphrase_bv):
    #     self.round_keys = []
    #     self.round_keys.append(self.find_round_key(passphrase_bv.get_bitvector_in_hex(), 0))
    #     for i in range(self.rounds - 1):
    #         self.round_keys.append(self.find_round_key(self.round_keys[i], i + 1))
    #     print(self.round_keys)
    #     return

    def encrypt(self, cipher_key: str, plaintext: str):
        result_cipher_text = ""
        cipher_key = self.handler_cipher_key(cipher_key)
        self.debug("Passphrase: %s" % cipher_key)
        cipher_key = BitVector(textstring=cipher_key)
        # gen round keys
        round_keys = self.expand_key(cipher_key.get_bitvector_in_hex())
        print(round_keys)
        # format plain text
        message = self.format_text(plaintext)
        self.debug("Plain text: %s" % message)
        start = 0  # diem bat dau cua segment
        end = 0  # diem ket thuc
        length = len(message)  # Do dai cua chuoi
        count_seg = math.ceil(length / 16)  # so cum 16 ky tu
        # duyet het cum 16 ky tu
        for x in range(count_seg):
            self.debug("Segment #%d" % (x + 1))
            if end + 16 < length:
                plaintext_seg = message[start:end + 16]
            else:
                plaintext_seg = message[start: length]
                plaintext_seg.ljust(16, '\0')
            # add cipher key
            result = self.add_round_key(BitVector(textstring=plaintext_seg).get_bitvector_in_hex(),
                                        round_keys[0])
            for y in range(self.rounds - 1):
                self.debug("Round #%d" % (y + 1))
                # hex_str = result_bv.get_bitvector_in_hex()

                # sub bytes
                result = self.sub_bytes(result)

                # shift row
                result = self.shift_rows(result)

                # mix column
                result = self.mix_columns(result)

                # add round key
                result = self.add_round_key(result, round_keys[y + 1])

            self.debug("Round #%d" % self.rounds)
            # Round last
            # hex_str = result_bv.get_bitvector_in_hex()

            # sub bytes
            result = self.sub_bytes(result)

            # shift row
            result = self.shift_rows(result)

            # add round key
            result = self.add_round_key(result, round_keys[self.rounds])

            # write hex
            result_cipher_text = result_cipher_text + result  # get_hex_string_from_bitvector

            # next segment
            start = start + 16
            end = end + 16

        return result_cipher_text

    def decrypt(self, cipher_key: str, ciphertext: str):
        result_plain_text = ""
        cipher_key = self.handler_cipher_key(cipher_key)
        print("Passphrase: %s" % cipher_key)
        cipher_key = BitVector(textstring=cipher_key)
        # gen round keys
        round_keys = self.expand_key(cipher_key.get_bitvector_in_hex())
        print("Cipher text: %s" % ciphertext)

        start = 0
        end = 32
        length = len(ciphertext)
        count_seg = math.ceil(length / 32)  # so cum 32 bit ( 2 bit 1 ky tu )
        for x in range(count_seg):
            self.debug("Segment #%d" % (x + 1))
            ciphertext_seg = ciphertext[start:end]

            # add round key
            result = self.add_round_key(hex_str=ciphertext_seg, round_key=round_keys[self.rounds])

            # inverse shift row
            result = self.inv_shift_rows(result)

            # inverse sub byte
            result = self.inv_sub_bytes(result)

            for y in range(self.rounds - 1, 0, -1):

                # add round key
                result = self.add_round_key(hex_str=result, round_key=round_keys[y])

                # mix column
                result = self.inv_mix_columns(result)

                # inverse shift row
                result = self.inv_shift_rows(result)

                # inverse sub byte
                result = self.inv_sub_bytes(result)

            # add cipher key
            result = self.add_round_key(hex_str=result, round_key=round_keys[0])

            # result = self.add_round_key(hex_str=ciphertext_seg, round_key=round_keys[0])
            #
            # for i in range(1, self.rounds):
            #     # inverse shift row
            #     result = self.inv_shift_rows(result)
            #
            #     # inverse subbytes
            #     result = self.inv_sub_bytes(result)
            #
            #     # inverse mix columns
            #     result = self.inv_mix_columns(result)
            #
            #     # add round key
            #     result = self.add_round_key(hex_str=result, round_key=round_keys[i])
            #
            # # inverse shift row
            # result = self.inv_shift_rows(result)
            #
            # # inverse sub bytes
            # result = self.inv_sub_bytes(result)
            #
            # # add round key
            # result = self.add_round_key(hex_str=result, round_key=round_keys[self.rounds])

            output_bv = BitVector(hexstring=self.inv_format_text(result))
            plaintext = output_bv.get_bitvector_in_ascii()
            plaintext = plaintext.replace('\x00', '')
            result_plain_text = result_plain_text + plaintext
            start = start + 32
            end = end + 32

        return result_plain_text

    @staticmethod
    def sub_bytes(hex_str):
        result = ""
        for loop in range(0, math.ceil(len(hex_str) / 2)):
            x = text_to_number(hex_str[loop * 2])
            y = text_to_number(hex_str[loop * 2 + 1])
            s_box_char = s_box_table[x][y]
            result = result + s_box_char
        return result

    @staticmethod
    def inv_sub_bytes(hex_str):
        result = ""
        for loop in range(0, math.ceil(len(hex_str) / 2)):
            x = text_to_number(hex_str[loop * 2])
            y = text_to_number(hex_str[loop * 2 + 1])
            s_box_char = iv_s_box_table[x][y]
            result = result + s_box_char
        return result

    @staticmethod
    def shift_rows(hex_str):
        if len(hex_str) == 8:
            result = hex_str[2:8] + hex_str[0:2]
            return result
        else:
            # Hang 1 giu nguyen 0 5 10 15
            result = hex_str[0:2] + hex_str[10: 12] + hex_str[20:22] + hex_str[30:32]
            # Hang 2 dich 1 byte 4 9 14 3
            result = result + hex_str[8:10] + hex_str[18:20] + hex_str[28:30] + hex_str[6:8]
            # Hang 3 dich 2 byte 8 13 2 7
            result = result + hex_str[16:18] + hex_str[26:28] + hex_str[4:6] + hex_str[14:16]
            # Hang 4 dich 3 byte 12 1 6 11
            result = result + hex_str[24:26] + hex_str[2:4] + hex_str[12:14] + hex_str[22:24]
            return result

    @staticmethod
    def inv_shift_rows(hex_str):
        if len(hex_str) == 8:
            result = hex_str[6:8] + hex_str[0:2] + hex_str[2:4] + hex_str[4:6]
            return result
        else:
            # Hang 1 giu nguyen 0 5 10 15
            result = hex_str[0:2] + hex_str[26:28] + hex_str[20:22] + hex_str[14:16]
            # Hang 2 dich 1 byte 4 9 14 3
            result = result + hex_str[8:10] + hex_str[2:4] + hex_str[28:30] + hex_str[22:24]
            # Hang 3 dich 2 byte 8 13 2 7
            result = result + hex_str[16:18] + hex_str[10:12] + hex_str[4:6] + hex_str[30:32]
            # Hang 4 dich 3 byte 12 1 6 11
            result = result + hex_str[24:26] + hex_str[18:20] + hex_str[12:14] + hex_str[6:8]
            return result

    @staticmethod
    def mix_columns(hex_str):
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

    @staticmethod
    def inv_mix_columns(hex_str):
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
        nine = BitVector(bitstring='1001')
        eleven = BitVector(bitstring='1011')
        thirteen = BitVector(bitstring='1101')
        fourteen = BitVector(bitstring='1110')

        tempbv1 = bv01.gf_multiply_modular(fourteen, eightlim, 8)  # done
        tempbv2 = bv23.gf_multiply_modular(eleven, eightlim, 8)
        tempbv3 = bv45.gf_multiply_modular(thirteen, eightlim, 8)
        tempbv4 = bv67.gf_multiply_modular(nine, eightlim, 8)
        newbv01 = tempbv1 ^ tempbv2 ^ tempbv3 ^ tempbv4

        tempbv1 = bv01.gf_multiply_modular(nine, eightlim, 8)  # done
        tempbv2 = bv23.gf_multiply_modular(fourteen, eightlim, 8)
        tempbv3 = bv45.gf_multiply_modular(eleven, eightlim, 8)
        tempbv4 = bv67.gf_multiply_modular(thirteen, eightlim, 8)
        newbv23 = tempbv1 ^ tempbv2 ^ tempbv3 ^ tempbv4

        tempbv1 = bv01.gf_multiply_modular(thirteen, eightlim, 8)  # done
        tempbv2 = bv23.gf_multiply_modular(nine, eightlim, 8)
        tempbv3 = bv45.gf_multiply_modular(fourteen, eightlim, 8)
        tempbv4 = bv67.gf_multiply_modular(eleven, eightlim, 8)
        newbv45 = tempbv1 ^ tempbv2 ^ tempbv3 ^ tempbv4

        tempbv1 = bv01.gf_multiply_modular(eleven, eightlim, 8)  # done
        tempbv2 = bv23.gf_multiply_modular(thirteen, eightlim, 8)
        tempbv3 = bv45.gf_multiply_modular(nine, eightlim, 8)
        tempbv4 = bv67.gf_multiply_modular(fourteen, eightlim, 8)
        newbv67 = tempbv1 ^ tempbv2 ^ tempbv3 ^ tempbv4

        tempbv1 = bv89.gf_multiply_modular(fourteen, eightlim, 8)  # done
        tempbv2 = bv1011.gf_multiply_modular(eleven, eightlim, 8)
        tempbv3 = bv1213.gf_multiply_modular(thirteen, eightlim, 8)
        tempbv4 = bv1415.gf_multiply_modular(nine, eightlim, 8)
        newbv89 = tempbv1 ^ tempbv2 ^ tempbv3 ^ tempbv4

        tempbv1 = bv89.gf_multiply_modular(nine, eightlim, 8)  # done
        tempbv2 = bv1011.gf_multiply_modular(fourteen, eightlim, 8)
        tempbv3 = bv1213.gf_multiply_modular(eleven, eightlim, 8)
        tempbv4 = bv1415.gf_multiply_modular(thirteen, eightlim, 8)
        newbv1011 = tempbv1 ^ tempbv2 ^ tempbv3 ^ tempbv4

        tempbv1 = bv89.gf_multiply_modular(thirteen, eightlim, 8)  # done
        tempbv2 = bv1011.gf_multiply_modular(nine, eightlim, 8)
        tempbv3 = bv1213.gf_multiply_modular(fourteen, eightlim, 8)
        tempbv4 = bv1415.gf_multiply_modular(eleven, eightlim, 8)
        newbv1213 = tempbv1 ^ tempbv2 ^ tempbv3 ^ tempbv4

        tempbv1 = bv89.gf_multiply_modular(eleven, eightlim, 8)  # done
        tempbv2 = bv1011.gf_multiply_modular(thirteen, eightlim, 8)
        tempbv3 = bv1213.gf_multiply_modular(nine, eightlim, 8)
        tempbv4 = bv1415.gf_multiply_modular(fourteen, eightlim, 8)
        newbv1415 = tempbv1 ^ tempbv2 ^ tempbv3 ^ tempbv4

        tempbv1 = bv1617.gf_multiply_modular(fourteen, eightlim, 8)  # done
        tempbv2 = bv1819.gf_multiply_modular(eleven, eightlim, 8)
        tempbv3 = bv2021.gf_multiply_modular(thirteen, eightlim, 8)
        tempbv4 = bv2223.gf_multiply_modular(nine, eightlim, 8)
        newbv1617 = tempbv1 ^ tempbv2 ^ tempbv3 ^ tempbv4

        tempbv1 = bv1617.gf_multiply_modular(nine, eightlim, 8)  # done
        tempbv2 = bv1819.gf_multiply_modular(fourteen, eightlim, 8)
        tempbv3 = bv2021.gf_multiply_modular(eleven, eightlim, 8)
        tempbv4 = bv2223.gf_multiply_modular(thirteen, eightlim, 8)
        newbv1819 = tempbv1 ^ tempbv2 ^ tempbv3 ^ tempbv4

        tempbv1 = bv1617.gf_multiply_modular(thirteen, eightlim, 8)  # done
        tempbv2 = bv1819.gf_multiply_modular(nine, eightlim, 8)
        tempbv3 = bv2021.gf_multiply_modular(fourteen, eightlim, 8)
        tempbv4 = bv2223.gf_multiply_modular(eleven, eightlim, 8)
        newbv2021 = tempbv1 ^ tempbv2 ^ tempbv3 ^ tempbv4

        tempbv1 = bv1617.gf_multiply_modular(eleven, eightlim, 8)  # done
        tempbv2 = bv1819.gf_multiply_modular(thirteen, eightlim, 8)
        tempbv3 = bv2021.gf_multiply_modular(nine, eightlim, 8)
        tempbv4 = bv2223.gf_multiply_modular(fourteen, eightlim, 8)
        newbv2223 = tempbv1 ^ tempbv2 ^ tempbv3 ^ tempbv4

        tempbv1 = bv2425.gf_multiply_modular(fourteen, eightlim, 8)  # done
        tempbv2 = bv2627.gf_multiply_modular(eleven, eightlim, 8)
        tempbv3 = bv2829.gf_multiply_modular(thirteen, eightlim, 8)
        tempbv4 = bv3031.gf_multiply_modular(nine, eightlim, 8)
        newbv2425 = tempbv1 ^ tempbv2 ^ tempbv3 ^ tempbv4

        tempbv1 = bv2425.gf_multiply_modular(nine, eightlim, 8)  # done
        tempbv2 = bv2627.gf_multiply_modular(fourteen, eightlim, 8)
        tempbv3 = bv2829.gf_multiply_modular(eleven, eightlim, 8)
        tempbv4 = bv3031.gf_multiply_modular(thirteen, eightlim, 8)
        newbv2627 = tempbv1 ^ tempbv2 ^ tempbv3 ^ tempbv4

        tempbv1 = bv2425.gf_multiply_modular(thirteen, eightlim, 8)  # done
        tempbv2 = bv2627.gf_multiply_modular(nine, eightlim, 8)
        tempbv3 = bv2829.gf_multiply_modular(fourteen, eightlim, 8)
        tempbv4 = bv3031.gf_multiply_modular(eleven, eightlim, 8)
        newbv2829 = tempbv1 ^ tempbv2 ^ tempbv3 ^ tempbv4

        tempbv1 = bv2425.gf_multiply_modular(eleven, eightlim, 8)  # done
        tempbv2 = bv2627.gf_multiply_modular(thirteen, eightlim, 8)
        tempbv3 = bv2829.gf_multiply_modular(nine, eightlim, 8)
        tempbv4 = bv3031.gf_multiply_modular(fourteen, eightlim, 8)
        newbv3031 = tempbv1 ^ tempbv2 ^ tempbv3 ^ tempbv4

        inv_mix_column_bv = newbv01 + newbv23 + newbv45 + newbv67 + newbv89 + newbv1011 + newbv1213 + newbv1415 + \
                            newbv1617 + newbv1819 + newbv2021 + newbv2223 + newbv2425 + newbv2627 + newbv2829 + \
                            newbv3031
        inv_mix_column_hex = inv_mix_column_bv.get_bitvector_in_hex()
        return inv_mix_column_hex

    @staticmethod
    def add_round_key(hex_str, round_key):
        # hex_str = text_str = round_key = round_key_bv = None
        # if 'hex_str' in kwargs:
        #     hex_str = kwargs.pop('hex_str')
        # if 'text_str' in kwargs:
        #     text_str = kwargs.pop('text_str')
        # if 'round_key' in kwargs:
        #     round_key = kwargs.pop('round_key')
        # if 'round_key_bv' in kwargs:
        #     round_key_bv = kwargs.pop('round_key_bv')
        #
        # bv = BitVector(hexstring=hex_str) if text_str is None else BitVector(textstring=text_str)
        # round_key_bv = BitVector(hexstring=round_key) if round_key_bv is None else round_key_bv
        bv = BitVector(hexstring=hex_str)
        round_key_bv = BitVector(hexstring=round_key)
        result_bv = bv ^ round_key_bv
        return result_bv.get_bitvector_in_hex()

    def handler_cipher_key(self, passphrase: str):
        passphrase_len = self.cipher_word * 4  # 1 word = 4 chu
        if len(passphrase) > passphrase_len:
            self.debug("Dai qua %d ky tu, cat bot." % passphrase_len)
            return passphrase[0:passphrase_len]
        if len(passphrase) < passphrase_len:
            self.debug("It hon %d ky tu, them khoang trang." % passphrase_len)
            return passphrase.ljust(passphrase_len, ' ')
            # Them khoang trang vao ben phai
        return passphrase

    @staticmethod
    def xor(hex1, hex2):
        bv1 = BitVector(hexstring=hex1)
        bv2 = BitVector(hexstring=hex2)
        bv3 = bv1 ^ bv2
        return bv3.get_bitvector_in_hex()

    def expand_key(self, cipher_key):
        r_con = ['01000000', '02000000', '04000000', '08000000', '10000000',
                 '20000000', '40000000', '80000000', '1b000000', '36000000',
                 '6c000000', 'd8000000', 'ab000000', '4d000000']
        max_word = (self.rounds + 1) * 4
        for n_w in range(self.cipher_word, max_word, 4):
            n_bit = n_w * 8
            # 1 word 8 bit hex
            before = cipher_key[n_bit - 8: n_bit]

            # Rotate word
            before = self.shift_rows(before)

            # sub bytes
            before = self.sub_bytes(before)

            # xor rcon
            before = self.xor(before, r_con[math.ceil(n_w / 4) - 1])

            for i in range(32, 0, -8):
                w = cipher_key[n_bit - i: n_bit - i + 8]
                w4 = self.xor(w, before)
                before = w4
                cipher_key = cipher_key + w4
        round_key = []
        for i in range(self.rounds + 1):
            round_key.append(cipher_key[i * 32: (i + 1) * 32])
        return round_key

    # def find_round_key(self, bv, case):
    #     r_con = ['01000000', '02000000', '04000000', '08000000', '10000000',
    #              '20000000', '40000000', '80000000', '1b000000', '36000000',
    #              '6c000000', 'd8000000', 'ab000000', '4d000000']
    #     # words
    #     w0 = bv[0:8]
    #     w1 = bv[8:16]
    #     w2 = bv[16:24]
    #     w3 = bv[24:32]
    #     # last word
    #     w = bv[24:32]
    #     # rotate word
    #     w = self.shift_rows(w)
    #     # sub bytes
    #     w = self.sub_bytes(w)
    #     # xor Rcon
    #     w = self.xor(w, r_con[case])
    #     w4 = self.xor(w0, w)
    #     w5 = self.xor(w1, w4)
    #     w6 = self.xor(w2, w5)
    #     w7 = self.xor(w3, w6)
    #     return w4 + w5 + w6 + w7

    @staticmethod
    def format_text(text: str):
        hex_str = BitVector(textstring=text).get_bitvector_in_hex()
        i = 0
        while i < len(hex_str):
            if hex_str[i: i + 2] == '0a':
                hex_str = hex_str[0: i] + '0d' + hex_str[i: len(hex_str)]
                i = i + 4
            else:
                i = i + 2
        new_txt = BitVector(hexstring=hex_str).get_bitvector_in_ascii()
        return new_txt

    @staticmethod
    def inv_format_text(hex_str: str):
        i = 0
        while i < len(hex_str):
            if hex_str[i:i + 2] == '0d':
                hex_str = hex_str[0:i] + hex_str[i + 2:len(hex_str)]
            else:
                i = i + 2
        return hex_str
