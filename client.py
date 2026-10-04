import socket 
HEADER=64
PORT=5050
FORMAT='utf-8'
DISCONNECT_MESSAGE="DISCONNECTED"
SERVER=socket.gethostbyname(socket.gethostname())
ADDR=(SERVER,PORT)
store={}#to actually store the data and it must persists across clients and acorss messages 
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)#connect to the server 

def send(msg):#to send message to the server 
    message=msg.encode(FORMAT) #encode the string in bytes like obj
    msg_length=len(message)
    send_length=str(msg_length).encode(FORMAT) #make the message length in utf format
    send_length+=b' '*(HEADER-len(send_length)) #padded the messags by adding blank spaces to make it of legnth 64
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))


send("TTL TEMP")