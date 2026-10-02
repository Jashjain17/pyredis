import socket 
import threading 


HEADER=64 #will tell the server that the first message should always be of size 64 that will tell us the size of the message that we are about to receive next 
PORT=5050
SERVER=socket.gethostbyname(socket.gethostname())
ADDR=(SERVER,PORT)
FORMAT='utf-8'
DISCONNECT_MESSAGE="DISCONNECTED"
store={}
lock=threading.lock()


server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)



def handle_client(conn,addr):

    print(f"[NEW CONNECTION] {addr} connected.")

    connected=True
    while connected:
        msg_length=conn.recv(HEADER).decode(FORMAT) #decode the message from btye format to a string using utf-8
        if msg_length:
            msg_length=int(msg_length)
            msg=conn.recv(msg_length).decode(FORMAT) #how many bites we will be receiving for the actual message 
            
            print(f"{addr} {msg}") #print out the user and their message
            parts=msg.split()# split the message into words — first word is the command, rest are arguments
            command=parts[0].upper()
            args=parts[1:]
            print(command,args)
            if command == "PING":
                response="PONG"
            elif command=="SET":
                key,value=args
                store[key]=value
                response="OK"
            elif command=="GET":
                key=args[0]
                response=store.get(key,("nil"))
            elif command=="DEL":
                key=args[0]
                existed=key in store
                store.pop(key,None)
                response="1" if existed else "0"
            elif command=="DISCONNECTED":
                response="DISCONNECTED"
                connected=False
            elif command=="INCR":
                key=args[0]
                with lock:
                    value=int(store.get(key,0))
                    value+=1
                    store[key]=str(value)
                    response=str(value)
  
            else:
                response="ERR unknown command"
 
            conn.send(response.encode(FORMAT)) #everytime we get a message we encode it and send it back
    conn.close() #close the connection   


def start(): #will allow server to listen to connections and handle those connenctions and will pass it to handle_client
    server.listen()
    print(f"Server is listening to {SERVER}")
    while True:
        conn,addr =server.accept() #we wait on this line for a new connection to the server and save its address(ip address and port)in addr as a tuple and then we will store an actual object that will allow us to send info back to the connection
        thread=threading.Thread(target=handle_client,args=(conn,addr)) #passing the new connection to handle client(target) with conn and addr as arguments
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}") # how many theads are active on this processor


print("Server is starting...")
start()