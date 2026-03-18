"""
Message Server with Classes and Exception Handling
This server accepts multiple clients and broadcasts messages between them.
"""

import socket
import threading
from colorama import Fore, Style, init
from typing import List, Tuple

# Initialize colorama for cross-platform colored output
init(autoreset=True)


class ConnectionError(Exception):
    """Custom exception for connection-related errors"""
    pass


class MessageServer:
    """
    A multi-client message server that broadcasts messages to all connected clients.
    
    Attributes:
        host (str): The IP address to bind the server to
        port (int): The port number to listen on
        server_socket (socket): The main server socket
        clients (List[Tuple[socket, str]]): List of connected client sockets and addresses
        running (bool): Flag to control server operation
    """
    
    def __init__(self, host: str = 'localhost', port: int = 5555):
        """
        Initialize the server with host and port.
        
        Args:
            host: IP address to bind to (default: localhost)
            port: Port number to listen on (default: 5555)
        """
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients: List[Tuple[socket.socket, str]] = []
        self.running = False
        self.client_lock = threading.Lock()  # Thread-safe access to clients list
        
    def start(self) -> None:
        """
        Start the server and begin listening for connections.
        
        Raises:
            ConnectionError: If server fails to bind to the specified port
        """
        try:
            # Create a TCP/IP socket
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Allow reuse of address (prevents "Address already in use" errors)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind socket to host and port
            self.server_socket.bind((self.host, self.port))
            
            # Listen for incoming connections (max 5 queued connections)
            self.server_socket.listen(5)
            
            self.running = True
            
            print(f"{Fore.GREEN}{'='*60}")
            print(f"{Fore.GREEN}🚀 Message Server Started!")
            print(f"{Fore.CYAN}📡 Listening on {self.host}:{self.port}")
            print(f"{Fore.YELLOW}⏳ Waiting for clients to connect...")
            print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}\n")
            
            # Accept client connections in a loop
            self.accept_clients()
            
        except OSError as e:
            raise ConnectionError(f"Failed to start server on {self.host}:{self.port} - {e}")
        except Exception as e:
            raise ConnectionError(f"Unexpected error starting server: {e}")
            
    def accept_clients(self) -> None:
        """
        Continuously accept new client connections.
        Each client is handled in a separate thread.
        """
        while self.running:
            try:
                # Accept a new client connection (blocks until a client connects)
                client_socket, client_address = self.server_socket.accept()
                
                # Add client to the list (thread-safe)
                with self.client_lock:
                    self.clients.append((client_socket, str(client_address)))
                
                print(f"{Fore.GREEN}✅ New client connected: {client_address}")
                print(f"{Fore.CYAN}👥 Total clients: {len(self.clients)}{Style.RESET_ALL}\n")
                
                # Create a new thread to handle this client
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address),
                    daemon=True  # Thread will close when main program exits
                )
                client_thread.start()
                
            except OSError:
                # Socket was closed, stop accepting
                if not self.running:
                    break
            except Exception as e:
                print(f"{Fore.RED}❌ Error accepting client: {e}{Style.RESET_ALL}")
                
    def handle_client(self, client_socket: socket.socket, client_address: Tuple) -> None:
        """
        Handle communication with a single client.
        Receives messages and broadcasts them to all other clients.
        
        Args:
            client_socket: The socket object for this client
            client_address: The address tuple (IP, port) of the client
        """
        try:
            # Send welcome message to the new client
            welcome_msg = "Welcome to the Message Server! Type your messages to chat.\n"
            client_socket.send(welcome_msg.encode('utf-8'))
            
            # Continuously receive and broadcast messages
            while self.running:
                try:
                    # Receive message from client (up to 1024 bytes)
                    message = client_socket.recv(1024).decode('utf-8')
                    
                    if not message:
                        # Empty message means client disconnected
                        break
                    
                    # Display message on server
                    print(f"{Fore.MAGENTA}📨 From {client_address}: {message.strip()}{Style.RESET_ALL}")
                    
                    # Broadcast message to all other clients
                    self.broadcast(f"[{client_address}]: {message}", client_socket)
                    
                except ConnectionResetError:
                    # Client forcefully closed connection
                    break
                except Exception as e:
                    print(f"{Fore.RED}⚠️  Error receiving from {client_address}: {e}{Style.RESET_ALL}")
                    break
                    
        finally:
            # Clean up: remove client and close socket
            self.remove_client(client_socket, client_address)
            
    def broadcast(self, message: str, sender_socket: socket.socket) -> None:
        """
        Send a message to all connected clients except the sender.
        
        Args:
            message: The message to broadcast
            sender_socket: The socket of the client who sent the message
        """
        with self.client_lock:
            disconnected_clients = []
            
            for client_socket, client_address in self.clients:
                # Don't send message back to the sender
                if client_socket != sender_socket:
                    try:
                        client_socket.send(message.encode('utf-8'))
                    except Exception as e:
                        print(f"{Fore.RED}❌ Failed to send to {client_address}: {e}{Style.RESET_ALL}")
                        disconnected_clients.append((client_socket, client_address))
            
            # Remove any clients that failed to receive the message
            for client_socket, client_address in disconnected_clients:
                self.remove_client(client_socket, client_address)
                
    def remove_client(self, client_socket: socket.socket, client_address: Tuple) -> None:
        """
        Remove a client from the active clients list and close their socket.
        
        Args:
            client_socket: The socket to close
            client_address: The address of the client being removed
        """
        with self.client_lock:
            # Remove from clients list if present
            for client in self.clients:
                if client[0] == client_socket:
                    self.clients.remove(client)
                    break
        
        # Close the socket
        try:
            client_socket.close()
        except:
            pass
            
        print(f"{Fore.YELLOW}👋 Client disconnected: {client_address}")
        print(f"{Fore.CYAN}👥 Total clients: {len(self.clients)}{Style.RESET_ALL}\n")
        
    def stop(self) -> None:
        """
        Gracefully shut down the server and close all connections.
        """
        print(f"\n{Fore.YELLOW}🛑 Shutting down server...{Style.RESET_ALL}")
        
        self.running = False
        
        # Close all client connections
        with self.client_lock:
            for client_socket, client_address in self.clients:
                try:
                    client_socket.close()
                except:
                    pass
            self.clients.clear()
        
        # Close server socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
                
        print(f"{Fore.GREEN}✅ Server stopped successfully{Style.RESET_ALL}")


def get_local_ip():
    """
    Get the local IP address of this machine.
    Returns a string like '192.168.1.100'
    """
    try:
        # Create a temporary socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Connect to an external address (doesn't actually send data)
        # This helps us determine which network interface to use
        s.connect(("8.8.8.8", 80))
        
        # Get our IP address
        ip_address = s.getsockname()[0]
        
        s.close()
        return ip_address
    except Exception:
        return "127.0.0.1"  # Fallback to localhost

def main():
    """
    Main function to create and start the server.
    Includes keyboard interrupt handling for graceful shutdown.
    """

    print(f"\n{Fore.CYAN}{'='*35}{Style.RESET_ALL}")
    my_ip = get_local_ip()
    print(f"{Fore.CYAN}Your IP address is: {my_ip} {Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*35}{Style.RESET_ALL}")

    # Set the IP address to bind to
    msg = f"\n{Fore.YELLOW}🙂 Enter the IP address of the server to connect to (default: {Fore.CYAN}{my_ip}{Fore.YELLOW}): {Style.RESET_ALL}"

    # ask user whether to use localhost or their local IP address
    myNew_ip = input(msg).strip() or my_ip
    if myNew_ip.lower() != my_ip.lower():
        my_ip = myNew_ip
    print(f"{Fore.GREEN}✅ Using IP address: {my_ip}{Style.RESET_ALL}")

    msg = f"{Fore.GREEN}✅ Connecting to server at {my_ip}:{5555}...{Style.RESET_ALL}"
    print(msg)

    # Create server instance
    # server = MessageServer(host='localhost', port=5555)
    server = MessageServer(host=my_ip, port=5555)
    
    try:
        # Start the server
        server.start()
    except ConnectionError as e:
        print(f"{Fore.RED}❌ Connection Error: {e}{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️  Keyboard interrupt received{Style.RESET_ALL}")
    finally:
        # Always stop the server gracefully
        server.stop()


if __name__ == "__main__":
    main()
