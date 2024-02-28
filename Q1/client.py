import pickle
import socket  

def send_file(file_path):
    """
    Function to read a file and serialize its data.
    
    Args:
        file_path (str): The path to the file to be read and sent.
        
    Returns:
        bytes: Serialized data containing the filename and file contents.
    """
    with open(file_path, 'r') as file:
        file_data = {'filename': file_path, 'data': file.read()}  
    return pickle.dumps(file_data)  #Pickling

def start_client():
    """
    Function to initiate the client-side communication with the server.
    """
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creating a TCP socket
        server_address = ('127.0.0.1', 12345)  # Setting the server address
        client_socket.connect(server_address)  # Connecting to the server

        file_path = input("Provide the file path of the file to be transferred: ")  
        serialized_data = send_file(file_path)  # Serializing file data
        client_socket.sendall(serialized_data)  # Sending serialized data to the server
        print("File sent to server.") 
    except Exception as err: # Error handling
        print(f"Error: {err}")  
    finally:
        client_socket.close()  # Closing the client socket

if __name__ == "__main__":
    start_client() 
