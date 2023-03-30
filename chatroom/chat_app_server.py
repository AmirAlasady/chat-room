import socket
import threading

 
#main sock --------------
HOST='127.0.0.1'
PORT=4444
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

#defs----------
def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
            print(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break
    
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()




thread2 = threading.Thread(target=receive)
thread2.start()
print('on - - - : ')


