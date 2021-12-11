from libary_aes.aes import subbyte,shiftrow,xor
def expand_key(cipher_key,cipher_word,rounds):
        r_con = ['01000000', '02000000', '04000000', '08000000', '10000000',
                 '20000000', '40000000', '80000000', '1b000000', '36000000',
                 '6c000000', 'd8000000', 'ab000000', '4d000000']
        max_word = (rounds + 1) * 4
        i = 0
        for n_w in range(cipher_word, max_word, 1):
            # Copy previous word
            n_bit = n_w * 8  # 1 word 8 bit hex
            word = cipher_key[n_bit - 8: n_bit]
            # Schedule_core mỗi 1 row
            if n_w % cipher_word == 0:
                # Rotate word
                word = shiftrow(word)

                # sub bytes
                word = subbyte(word)

                # xor Rcon
                word = xor(word, r_con[i])
                # increase i
                i = i + 1
            elif cipher_word == 8 and n_w % cipher_word == 4:
                # Sub bytes mỗi 4 word khi sử dụng
                # 256-bit key.
                word = subbyte(word)

            # Word tương đương
            previous = cipher_key[(n_w - cipher_word) * 8: (n_w - cipher_word + 1) * 8]
            # Xor với word tương đương
            word = xor(word, previous)
            # Nối vào
            cipher_key = cipher_key + word
        # Trả về các tập hợp 32bit = 4 word = 1 round key
        return [cipher_key[32 * i: 32 * (i + 1)] for i in range(len(cipher_key) // 32)]

cipher_key = "3031323334353637383940414243444530313233343536373839404142434445"
cipher_word = 8
rounds = 14
print(expand_key(cipher_key,cipher_word,rounds))
