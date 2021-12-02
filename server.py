import socket
from libary_aes.decrypt import AES_decrypt

def server_program():
    # get the hostname
    host = socket.gethostname() # Lấy địa chi IP của máy tính đang sử dụng
    port = 8080  # initiate port no above 1024
    FORMAT = "utf8"

    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # get instance
    '''
        SOCK_STREAM là dùng giao thức TCP

    '''
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together
    '''
    host cái server trên địa chỉ khai báo
    '''

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    # lắng nghe 
    print(" chờ client kết nối")
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))
        wf = open('libary_aes/XauMa1.txt',mode = 'w',encoding = 'utf-8')
        wf.write("heloo")
        KeyCharacter = input(" nhập ký tự khóa : ")
        key =  input(" Khóa ")
        message = AES_decrypt.file_decrypt('libary_aes/XauMa1.txt','libary_aes/XauRo1.txt',KeyCharacter,key)
        # data = input(' -> ')c
        conn.send(message.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()