import socket 
import threading 


HEADER=64 #will tell the server that the first message should always be of size 64 that will tell us the size of the message that we are about to receive next 

PORT=5050
SERVER=socket.gethostbyname(socket.gethostname())
ADDR=(SERVER,PORT)
FORMAT='utf-8'
DISCONNECT_MESSAGE="DISCONNECTED"
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected=True
    while connected:
        msg_length=conn.recv(HEADER).decode(FORMAT) #decode the message from btye format to a string using utf-8
        msg_length=int(msg_length)
        msg=conn.recv(msg_length).decode(FORMAT) #how many bites we will be receiving for the actual message 
        if msg==DISCONNECT_MESSAGE: # condition to know client wants to disconnect 
            connected=False

        print(f"{addr} {msg}") #print out the user and their message
    conn.close() #close the connection    
def start(): #will allow server to listen to connections and handle those connenctions and will pass it to handle_client
    server.listen()
    print(f"Server is listening to {SERVER}")
    while True:
        conn,addr =server.accept() #we wait on this line for a new connection to the server and save its address(ip address and port) and then we will store and actual object that will allow us to send info back to the connection
        thread=threading.Thread(target=handle_client,args=(conn,addr)) #passing the new connection to handle client(target) with conn and addr as arguments
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}") # how many theads are active on this processor
print("Server is starting...")
start()