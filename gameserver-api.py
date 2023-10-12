import socket

# Define host and port for your server
host = '0.0.0.0'  # Listen on all available network interfaces
port = 12345      # Choose an available port

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server_socket.bind((host, port))

# Listen for incoming connections (max 5)
server_socket.listen(10)
teams = [31,32,33]

print(f"Server is listening on {host}:{port}")

while True:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    
    client_socket.send(b"Welcome to the gameserver api, pls chose one of the following:\n1. Check the status of your services.\n2. Launch attack against one of your services.\n")
    # Receive data from the client
    data = client_socket.recv(1024).decode('utf-8')

    if "1" in data:
        client_socket.send(b"What is the team-id (digits of the IP) you want to check?\n")
        client_socket.send(b"Checking your services of %s...."%target.encode("utf-8"))
        try:
            teamid = int(client_socket.recv(1024).decode("utf-8").strip())
            if teamid not in teams:
                client_socket.send(b"Teamid not valid")
            else:
                target = "192.168.42."+str(teamid)
        except:
            client_socket.send(b"Teamid not valid")

        try:
            run_saarxiv_check(teamid,1)
            client_socket.send(b"SaarXiv: UP")
        except:
            client_socket.send(b"SaarXiv: DOWN")
        
        try:
            run_saarlender_check(teamid,1)
            client_socket.send(b"Saarlenar: UP")
        except: 
            client_socket.send(b"Saarlenar: DOWN")

    if "2" in data:
        client_socket.send(b"Against which service should the gameserver launch an attack?\n1. SaarXiv\n2. Saarlendar\n")
        service = client_socket.recv(1024).decode('utf-8')
        if "1" in service:
            exploit_saarxiv(teamid)
        elif "2" in data:
            exploit_saarlendar(teamid)
        
        


        #check_services()
    # Add your code to process the command here
    # For security, make sure to validate and sanitize the received command.

    # Example: Echo the command back to the client
    #client_socket.send(response.encode('utf-8'))

    # Close the client socket
    client_socket.close()

# Close the server socket (this part of the code may never be reached in practice)
server_socket.close()
