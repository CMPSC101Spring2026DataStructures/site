"""
Message Client with Classes and Exception Handling
This client connects to a message server and allows real-time communication.
"""

import socket
import threading
from colorama import Fore, Back, Style, init
from typing import Optional

# Initialize colorama
init(autoreset=True)


class NetworkError(Exception):
    """Custom exception for network-related errors"""
    pass


class MessageClient:
    """
    A message client that connects to a server and enables real-time chat.
    
    Attributes:
        host (str): Server IP address to connect to
        port (int): Server port number
        client_socket (socket): The socket connection to the server
        username (str): Display name for this client
        connected (bool): Connection status flag
    """
    
    def __init__(self, host: str = 'localhost', port: int = 5555, username: str = "User"):
        """
        Initialize the client with connection parameters.
        
        Args:
            host: Server IP address to connect to
            port: Server port number
            username: Display name for this user
        """
        self.host = host
        self.port = port
        self.client_socket: Optional[socket.socket] = None
        self.username = username
        self.connected = False
        
    def connect(self) -> None:
        """
        Establish connection to the server.
        
        Raises:
            NetworkError: If connection fails
        """
        try:
            # Create TCP/IP socket
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Set a timeout for connection attempt (10 seconds)
            self.client_socket.settimeout(10)
            print(f"{Fore.YELLOW}🔍 Attempting to connect to server at {self.host} {Style.RESET_ALL}")
            print(f"{Fore.CYAN}🔌 Connecting to server at {self.host}:{self.port}...{Style.RESET_ALL}")
            
            # Connect to the server
            self.client_socket.connect((self.host, self.port))
            
            # Remove timeout for normal operations
            self.client_socket.settimeout(None)
            
            self.connected = True
            
            # Display colorful welcome
            print(f"\n{Back.GREEN}{Fore.BLACK}{'='*60}{Style.RESET_ALL}")
            print(f"{Back.GREEN}{Fore.BLACK}  ✅ CONNECTED TO MESSAGE SERVER!  {Style.RESET_ALL}")
            print(f"{Back.GREEN}{Fore.BLACK}{'='*60}{Style.RESET_ALL}\n")
            print(f"{Fore.YELLOW}👤 Username: {Fore.WHITE}{self.username}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}💬 You can now start chatting!")
            print(f"{Fore.CYAN}📤 Type your message and press Enter to send")
            print(f"{Fore.RED}🚪 Type 'quit' or 'exit' to disconnect\n")
            print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}\n")
            
        except socket.timeout:
            raise NetworkError(f"Connection timed out. Is the server running on {self.host}:{self.port}?")
        except ConnectionRefusedError:
            raise NetworkError(f"Connection refused. Make sure the server is running on {self.host}:{self.port}")
        except socket.gaierror:
            raise NetworkError(f"Invalid host address: {self.host}")
        except Exception as e:
            raise NetworkError(f"Failed to connect to server: {e}")
            
    def send_messages(self) -> None:
        """
        Continuously read user input and send messages to the server.
        Runs in a separate thread.
        """
        while self.connected:
            try:
                # Read user input
                message = input()
                
                # Check for quit commands
                if message.lower() in ['quit', 'exit']:
                    print(f"{Fore.YELLOW}👋 Disconnecting...{Style.RESET_ALL}")
                    self.disconnect()
                    break
                
                # Don't send empty messages
                if not message.strip():
                    continue
                
                # Format message with username
                formatted_message = f"[{self.username}]: {message}"
                
                # Send to server
                self.client_socket.send(formatted_message.encode('utf-8'))
                
                # Display your own message in a different color
                print(f"{Fore.LIGHTBLUE_EX}📤 You: {message}{Style.RESET_ALL}")
                
            except OSError:
                # Socket was closed
                if not self.connected:
                    break
            except Exception as e:
                if self.connected:
                    print(f"{Fore.RED}❌ Error sending message: {e}{Style.RESET_ALL}")
                    self.disconnect()
                break
                
    def receive_messages(self) -> None:
        """
        Continuously receive messages from the server and display them.
        Runs in a separate thread.
        """
        while self.connected:
            try:
                # Receive message from server (up to 1024 bytes)
                message = self.client_socket.recv(1024).decode('utf-8')
                
                if not message:
                    # Empty message means server closed connection
                    print(f"\n{Fore.RED}❌ Server closed the connection{Style.RESET_ALL}")
                    self.disconnect()
                    break
                
                # Display received message with color
                # Check if it's a welcome message vs. a user message
                if message.startswith("Welcome"):
                    print(f"{Fore.GREEN}🎉 {message}{Style.RESET_ALL}")
                else:
                    # Parse and display user messages
                    print(f"{Fore.LIGHTGREEN_EX}📨 {message.strip()}{Style.RESET_ALL}")
                
            except OSError:
                # Socket was closed
                if not self.connected:
                    break
            except Exception as e:
                if self.connected:
                    print(f"{Fore.RED}❌ Error receiving message: {e}{Style.RESET_ALL}")
                    self.disconnect()
                break
                
    def start(self) -> None:
        """
        Start the client by connecting and launching send/receive threads.
        """
        try:
            # Connect to server
            self.connect()
            
            # Create thread for receiving messages
            receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
            receive_thread.start()
            
            # Use main thread for sending messages (so input() works properly)
            self.send_messages()
            
        except NetworkError as e:
            print(f"{Fore.RED}❌ Network Error: {e}{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}⚠️  Keyboard interrupt received{Style.RESET_ALL}")
            self.disconnect()
        except Exception as e:
            print(f"{Fore.RED}❌ Unexpected error: {e}{Style.RESET_ALL}")
            self.disconnect()
            
    def disconnect(self) -> None:
        """
        Gracefully disconnect from the server.
        """
        if not self.connected:
            return
            
        self.connected = False
        
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
                
        print(f"\n{Fore.YELLOW}{'='*60}")
        print(f"👋 Disconnected from server")
        print(f"{'='*60}{Style.RESET_ALL}\n")


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
    Main function to create and start the client.
    Prompts user for their username before connecting.
    """
    # Display colorful banner
    print(f"\n{Back.CYAN}{Fore.BLACK}{'='*60}{Style.RESET_ALL}")
    print(f"{Back.CYAN}{Fore.BLACK}  🌟 WELCOME TO THE MESSAGE CLIENT! 🌟  {Style.RESET_ALL}")
    print(f"{Back.CYAN}{Fore.BLACK}{'='*60}{Style.RESET_ALL}\n")

    print(f"\n{Fore.CYAN}{'='*35}{Style.RESET_ALL}")
    my_ip = get_local_ip()
    print(f"{Fore.CYAN}Your IP address is: {my_ip} {Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*35}{Style.RESET_ALL}")

    # Get username from user
    username = input(f"{Fore.YELLOW}Enter your username: {Style.RESET_ALL}").strip()
    
    # Use default if empty
    if not username:
        username = "Anonymous"
    
    print(f"{Fore.GREEN}✅ Username set to: {username}{Style.RESET_ALL}\n")
    
    # Get the IP address to connect to
    msg = f"\n{Fore.YELLOW}🙂 Enter the IP address of the server to connect to (default: {Fore.CYAN}{my_ip}{Fore.YELLOW}): {Style.RESET_ALL}"

    # ask user whether to use localhost or their local IP address
    myNew_ip = input(msg).strip() or my_ip
    if myNew_ip.lower() != my_ip.lower():
        my_ip = myNew_ip
    print(f"{Fore.GREEN}✅ Using IP address: {my_ip}{Style.RESET_ALL}")

    msg = f"{Fore.GREEN}✅ Connecting to server at {my_ip}:{5555}...{Style.RESET_ALL}"
    print(msg)

    # Create and start client
    # client = MessageClient(host='localhost', port=5555, username=username)
    client = MessageClient(host=my_ip, port=5555, username=username)
    client.start()


if __name__ == "__main__":
    main()
