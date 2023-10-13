import socket
import redis
from gamelib import *

# Define host and port for your server
host = '0.0.0.0'  # Listen on all available network interfaces
port = 6666      # Choose an available port

# Initialize a Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def check_flag(flag_data):
    try:
        # Check if the flag is already in Redis
        if redis_client.get(flag_data):
            return (False, "Flag already submitted")

        flag_checker = ServiceInterface(7)
        res = flag_checker.check_flag(flag_data)

        if res[0]:
            # Store the flag in Redis with a value of "1" to mark it as submitted
            redis_client.set(flag_data, 1)

        return res

    except Exception as e:
        return (False, str(e))

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

                while True:
                    try:
                        # Receive data from the client with a timeout
                        data = client_socket.recv(1024).decode('utf-8').strip()

                        if not data:
                            # No data received, handle this case if needed
                            client_socket.close()
                            break

                        # Perform flag checking
                        res = check_flag(data)

                        # Send response to the client
                        if res[0]:
                            client_socket.send("Flag accepted\n".encode('utf-8'))
                        else:
                            client_socket.send(f"Flag not valid: {res[1]}\n".encode('utf-8'))

                    except socket.timeout:
                        print("Timeout: No data received from the client within 10 seconds")
                        break

                    except Exception as e:
                        print(f"Error: {str(e)}")
                        client_socket.send(f"An error occurred: {str(e)}\n".encode('utf-8'))
                        break

            except socket.timeout:
                print("Timeout: No client connection within 10 seconds")
                continue

            except Exception as e:
                print(f"Error: {str(e)}")

    except Exception as e:
        print(f"Server Error: {str(e)}")

    finally:
        # Close the server socket (this part of the code may never be reached in practice)
        server_socket.close()

if __name__ == "__main__":
    main()
