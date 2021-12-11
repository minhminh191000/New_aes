import socket
from libary_aes.encrypt import AES_encrypt
import tkinter as tk
from tkinter import *
from tkinter import messagebox



selected = 0
public_key = None
cipher_text = None
plain_text = None
class App(tk.Tk):
    def __init__(self):
        box2 = None
        tk.Tk.__init__(self)
        self.iconbitmap('LogoXP.ico')
        self.geometry("800x500+150+150")
        self.resizable(False,False) 
        self.title("Migor")
        Header = Label(self, text="Welcome to Client",font="arial 15 bold")
        Header.pack()
        Header1 = Label(self, text="Migor",font="arial 15 bold")
        Header1.pack()
        #=========================
        Label_box1 = Label(self, text="Bản Rõ",font="arial 12")
        Label_box1.place(x=90,y=80)
        global plain_text
        plain_text = Text(self,height=15,width=30)
        plain_text.place(x=5,y=110)
        #=============================
        

        Label_box2 = Label(self, text="Ký tự khóa",font="arial 12")
        Label_box2.place(x=360,y=80)
        global public_key
        public_key = Text(self,height=10,width=25)
        public_key.place(x=300,y=110)
        #=================================
        def in_var():
            global selected
            choose = var.get()
            if choose == 1:
                selected = "128"
            elif choose == 2:
                selected = "192"
            elif choose == 3:
                selected = "256"
            # print(var.get())
        var = IntVar()
        Radiobutton(self, text="128", variable=var, value=1, command=in_var).place(x=340,y=300)
        Radiobutton(self, text="192", variable=var, value=2, command=in_var).place(x=390,y=300)
        Radiobutton(self, text="256", variable=var, value=3, command=in_var).place(x=440,y=300)
        
        

        #=====================
        global cipher_text
        Label_box4 = Label(self, text="Bản Mã",font="arial 12")
        Label_box4.place(x=640,y=80)
        cipher_text = Text(self,height=15,width=30)
        cipher_text.place(x=550,y=110)
        
        #=====================
        ''' button '''
        SaveFile = Button(self, text="Save",fg="red",font="arial 13",borderwidth=5, command=self.save_file)
        SaveFile.place(x=100 , y =400)
        #=====================
        Encode = Button(self, text="Encode",fg="red",font="arial 13",borderwidth=5, command=self.encode)
        Encode.place(x=350 , y =400)
        #=====================
        Send = Button(self, text="Send",fg="red",font="arial 13",borderwidth=5,command=self.send_file)
        Send.place(x=600 , y=400)



    def save_file(event):
        f = open('libary_aes/XauRo.txt',mode = 'w',encoding = 'utf-8')
        f.write(plain_text.get("1.0", "end"))
        f.close() 
        messagebox.showinfo(title="save",message="file saved")

    def encode(event):
        cipher_text.delete(1.0, END)
        key = selected
        KeyCharacter = public_key.get("1.0", "end")
        # print("đã vào")
        AES_encrypt.file_encrypt('libary_aes/XauRo.txt','libary_aes/XauMa.txt',KeyCharacter,key)
        f = open('libary_aes/XauMa.txt',mode = 'r',encoding = 'utf-8')
        message = f.read()
        cipher_text.insert("end",message)
        messagebox.showinfo(title="client",message="Encode Done")
    def send_file(event):
        # messagebox.showinfo(title="client",message="Send Cipher Text")
        host = socket.gethostname()  # as both code is running on same pc
        port = 8080  # socket server port number
        client_socket = socket.socket()  # instantiate
        client_socket.connect((host, port))  # connect to the server
        # print("da vap")
        f = open('libary_aes/XauMa.txt',mode = 'r',encoding = 'utf-8')
        message = f.read()
        client_socket.send(message.encode())  # send message
        # print("da gui")
        # data = client_socket.recv(1024).decode()  # receive response
        # print('Received from server: ' + data)  # show in terminal
    


def client_manage():
    KeyCharacter = input(" nhập ký tự khóa : ")
    key =  input(" Khóa ")
    AES_encrypt.file_encrypt('libary_aes/XauRo.txt','libary_aes/XauMa.txt',KeyCharacter,key)
    client_program()
    return 

def read_file():
    pass

def client_program():
    pass


if __name__ == '__main__':
    app = App()
    app.mainloop()