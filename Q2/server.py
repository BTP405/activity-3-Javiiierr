import socket
import pickle
import threading

class TaskQueueWorker:
    def __init__(self, host, port):
        """
        Initialize a TaskQueueWorker object
        
        Arguments:
        - host (str): The hostname or IP address to bind the worker to.
        - port (int): The port number to bind the worker to.
        """
        self.host = host
        self.port = port

    def start(self):
        """
        Start the worker node to listen for incoming tasks.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port)) 
            s.listen()  
            print(f"Worker listening on {self.host}:{self.port}")
            while True:
                conn, addr = s.accept()  # Accept connection
                with conn:
                    print(f"Connected by {addr}")
                    data = conn.recv(4096)  # receive task data
                    task = pickle.loads(data)  # Unpickle task data
                    result = self.execute_task(task)  # Execute task
                    conn.sendall(pickle.dumps(result))  # Send result back

    def execute_task(self, task):
        """
        Execute the task received by the worker.
        
        Arguments:
        - task (dict): A dictionary representing the task to be executed. 
                      It should have keys: 'function', 'args', and 'kwargs'.
        
        Returns:
        - The result of executing the task.
        """
        function = task['function']
        args = task['args']
        kwargs = task['kwargs']
        result = function(*args, **kwargs)  # Call function with arguments
        return result

class TaskQueueClient:
    def __init__(self, worker_nodes):
        """
        Initialize a TaskQueueClient object.
        
        Arguments:
        - worker_nodes (list of tuples): List of tuples containing the addresses 
                                         (hostname, port) of worker nodes.
        """
        self.worker_nodes = worker_nodes

    def distribute_task(self, task):
        """
        Distribute a task to all worker nodes and collect results.
        
        Arguments:
        - task (dict): A dictionary representing the task to be distributed. 
                      It should have keys: 'function', 'args', and 'kwargs'.
        
        Returns:
        - A list of results from executing the task on each worker node.
        """
        results = []
        for node in self.worker_nodes:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.connect(node)  # Connect to worker node
                    s.sendall(pickle.dumps(task))  # Send task data
                    data = s.recv(4096)  # Receive result
                    result = pickle.loads(data)  # Unpickle result
                    results.append(result)  # Store result
                except Exception as e:
                    print(f"Error executing task on {node}: {e}")  # Handle errors
        return results

def add(a, b):
    """
    Add two numbers.
    
    Arguments:
    - a (int/float): First number.
    - b (int/float): Second number.
    
    Returns:
    - The sum of a and b.
    """
    return a + b

if __name__ == "__main__":
    # Start worker nodes
    worker1 = TaskQueueWorker('localhost', 5000)
    worker2 = TaskQueueWorker('localhost', 5001)
    threading.Thread(target=worker1.start).start()  # Start worker 1 
    threading.Thread(target=worker2.start).start()  # Start worker 2 

    # Define tasks
    task1 = {'function': add, 'args': (5, 3), 'kwargs': {}}  
    task2 = {'function': add, 'args': (10, 20), 'kwargs': {}}  

    # Create client and distribute tasks
    client = TaskQueueClient([('localhost', 5000), ('localhost', 5001)])  # Client with worker node addresses
    results = client.distribute_task(task1)  # Distribute task 1
    print("Results of task 1:", results)
    results = client.distribute_task(task2)  # Distribute task 2
    print("Results of task 2:", results)
