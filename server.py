import socket
from libary_aes.decrypt import AES_decrypt
from tkinter import *
from tkinter import  messagebox

from PIL import ImageTk, Image
import tkinter as tk



selected = 0
public_key = None
cipher_text = None
text = None

class App(tk.Tk):
    
    def __init__(self):
        box2 = None
        tk.Tk.__init__(self)
        self.iconbitmap('LogoXP.ico')
        self.geometry("800x500+300+100")
        self.resizable(False,False) 
        self.title("Migor Server")
        Header = Label(self, text="Welcome to Server",font="arial 15 bold")
        Header.pack()
        Header1 = Label(self, text="Migor",font="arial 15 bold")
        Header1.pack()
        #=========================
        Label_box1 = Label(self, text="Bản Mã",font="arial 12")
        Label_box1.place(x=90,y=80)
        global text
        text = Text(self,height=15,width=30)
        text.place(x=5,y=110)
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
        Label_box4 = Label(self, text="Bản Rõ",font="arial 12")
        Label_box4.place(x=640,y=80)
        cipher_text = Text(self,height=15,width=30)
        cipher_text.place(x=550,y=110)
        
        #=====================
        ''' button '''
        take = Button(self, text="take",fg="red",font="arial 13",borderwidth=5, command=self.take)
        take.place(x=100 , y =400)
        #=====================
        decrypt = Button(self, text="decrypt",fg="red",font="arial 13",borderwidth=5, command=self.decrypt)
        decrypt.place(x=350 , y =400)
        #=====================
        server = Button(self, text="server",fg="red",font="arial 13",borderwidth=5,command=self.server)
        server.place(x=600 , y=400)


    def save_file(event):
        
        pass

    def decrypt(event):
        cipher_text.delete(1.0, END)
        # text.delete(1.0, END)
        key = selected
        KeyCharacter = public_key.get("1.0", "end")
        print("đã vào")
        AES_decrypt.file_decrypt('libary_aes/XauMa.txt','libary_aes/XauRo1.txt',KeyCharacter,key)
        f = open('libary_aes/XauRo1.txt',mode = 'r',encoding = 'utf-8')
        message = f.read()
        cipher_text.insert("end",message)
        messagebox.showinfo(title="Server",message="Decrypt done")
    def take(event): 
        text.delete(1.0, END)
        wf = open('libary_aes/XauMa1.txt',mode = 'r',encoding = 'utf-8')
        data = wf.read()
        print(data)
        text.insert("end",data)
        messagebox.showinfo(title="Server",message="Read data")
        
        pass
    def server(event):
        messagebox.showinfo(title="Server",message="Server to client")
        host = socket.gethostname() # Lấy địa chi IP của máy tính đang sử dụng
        port = 8080  # initiate port no above 1024
        FORMAT = "utf8"
        server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # get instance
        server_socket.bind((host, port))  # bind host address and port together
        # configure how many client the server can listen simultaneously
        server_socket.listen(2)
        # lắng nghe 
        print(" chờ client kết nối")
        conn, address = server_socket.accept()  # accept new connection
        print("Connection from: " + str(address))
        data = conn.recv(1024).decode()
        print(data)
        print("from connected user: data transmitted to")
        wf = open('libary_aes/XauMa1.txt',mode = 'w',encoding = 'utf-8')
        wf.write(data)
        wf.close()
        messagebox.showinfo(title="Server",message="Client connect")
        # print("da luu vao file")
    
        



if __name__ == '__main__':
    app = App()
    app.mainloop()
    # server_program()
