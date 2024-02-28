import pickle 
import os  
import socket  

def save_file(data, directory):
    """
    Function to save received file data to a specified directory.
    
    Args:
        data (dict): Dictionary containing filename and file contents.
        directory (str): The directory where the file will be saved.
    """
    file_name  = os.path.basename(data['filename'])  # Filename from the received data.
    file_path = os.path.join(directory, file_name)  # Full file path
    with open(file_path, 'w') as f:
        f.write(data['data'])  
    print(f"File saved to: {file_path}")  

def start_server():
    """
    Function to start the server and handle incoming connections.
    """
    # Creating socket, setting address, binding, listening
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server_address = ('127.0.0.1', 12345)  
    server_socket.bind(server_address)  
    server_socket.listen(1)  

    print("Listening for connections...")  
    while True:
        client_socket, client_address = server_socket.accept()  # Accepting incoming connections
    
        try:
            print("Connected to: ", client_address)
            save_dir = input("Specify the directory where the received file will be saved: ")  
            os.makedirs(save_dir, exist_ok=True)  
            
            file_received = client_socket.recv(4096)  
            file_data = pickle.loads(file_received)  # Unpickling the received data
            save_file(file_data, save_dir)  # Savingg to the specified directory.
        except Exception as error: # Error handling
            print(f"Error: {error}") 
        finally:
            client_socket.close()  

if __name__ == "__main__":
    start_server()  
