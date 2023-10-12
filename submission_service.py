import socket
from gamelib import *
import redis

# Define host and port for your server
host = '0.0.0.0'  # Listen on all available network interfaces
port = 6666      # Choose an available port


def check_flag():
    return True

def main():

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set a timeout for client connections (5 seconds, for example)
    server_socket.settimeout(10)

    try:
        # Bind the socket to the host and port
        server_socket.bind((host, port))

        # Listen for incoming connections (max 20)
        server_socket.listen(20)

        print(f"Server is listening on {host}:{port}")

        while True:
            try:
                # Accept a client connection
                client_socket, client_address = server_socket.accept()
                
                client_socket.send(b"Welcome to the submission server, please submit one flag per line:\n")

                # Receive data from the client with a timeout
                data = client_socket.recv(1024).decode('utf-8').strip()

                if not data:
                    # No data received, handle this case if needed
                    client_socket.close()
                    continue

                # Perform flag checking
                flag_checker = ServiceInterface(7)
                res = flag_checker.check_flag(data)
                
                # Send response to the client
                if res[0]:
                    client_socket.send("Flag accepted\n".encode('utf-8'))
                else:
                    client_socket.send("Flag not valid\n".encode('utf-8'))

            except socket.timeout:
                print("Timeout: No client connection within 5 seconds")

            except Exception as e:
                print(f"Error: {str(e)}")
                client_socket.close()


    except Exception as e:
        print(f"Server Error: {str(e)}")

    finally:
        # Close the server socket (this part of the code may never be reached in practice)
        server_socket.close()


if __name__ == "__main__":
    main()
