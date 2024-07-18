import socket
import threading

# Lista para armazenar os clientes conectados
clients = []
usernames = []

# Senha para entrar no chat
PASSWORD = "senha123"

# Função para gerenciar as mensagens recebidas dos clientes
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                if message.lower() == "sair":
                    remove(client_socket)
                    break
                username = usernames[clients.index(client_socket)]
                broadcast(f"{username}: {message}", client_socket)
            else:
                remove(client_socket)
                break
        except:
            continue

# Função para enviar mensagens para todos os clientes conectados
def broadcast(message, client_socket):
    for client in clients:
        try:
            client.send(message.encode('utf-8'))
        except:
            remove(client)

# Função para remover um cliente da lista de clientes conectados
def remove(client_socket):
    if client_socket in clients:
        index = clients.index(client_socket)
        clients.remove(client_socket)
        client_socket.close()
        username = usernames[index]
        broadcast(f"{username} saiu do chat :(", client_socket)
        usernames.remove(username)
        update_members_list()

# Função para atualizar a lista de membros conectados
def update_members_list():
    members_list = f"(Membros ON no chat: {', '.join(usernames)})"
    broadcast(members_list, None)

# Configurações do servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 9090))
server.listen(5)

print("Servidor iniciado e aguardando conexões...")

while True:
    client_socket, client_address = server.accept()
    print(f"Conexão estabelecida com {client_address}")

    client_socket.send("PASSWORD".encode('utf-8'))
    password = client_socket.recv(1024).decode('utf-8')

    if password == PASSWORD:
        client_socket.send("USERNAME".encode('utf-8'))
        username = client_socket.recv(1024).decode('utf-8')
        usernames.append(username)
        clients.append(client_socket)

        print(f"Username do client é {username}")
        broadcast(f"{username} entrou no chat", client_socket)
        client_socket.send("Bem vindo ao chat da sala 302, vamos fofocar!".encode('utf-8'))
        update_members_list()

        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()
    else:
        client_socket.send("senha incorreta".encode('utf-8'))
        client_socket.close()
