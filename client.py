import socket
import threading

# Função para receber mensagens do servidor
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == 'PASSWORD':
                client_socket.send(password.encode('utf-8'))
            elif message == 'USERNAME':
                client_socket.send(username.encode('utf-8'))
            elif message == 'senha incorreta':
                print("senha incorreta")
                client_socket.close()
                break
            else:
                print(message)
        except:
            print("An error occurred.")
            client_socket.close()
            break

# Função para enviar mensagens para o servidor
def send_message(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))
        if message.lower() == "sair":
            client_socket.close()
            break

# Configurações do cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 9090))

password = input("Digite a senha para entrar no chat: ")
username = input("Seu username: ")

# Thread para receber mensagens do servidor
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

# Thread para enviar mensagens para o servidor
send_thread = threading.Thread(target=send_message, args=(client_socket,))
send_thread.start()
