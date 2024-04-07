import socket
import threading

from src.app.clientstore import ClientStore
from src.app.commands.commandContext import CommandContext
from src.app.commands.commandHandler import CommandHandler
from src.app.infostore import InfoStore
from src.app.keystore import KeyStore
from src.app.parser import Parser

HEADER: int = 1024

DISCONNECT_MESSAGE: str = "!DISCONNECT"


class Redis:
    def __init__(self, args: list) -> None:
        self.parser: Parser = Parser()
        self.info_store = InfoStore()
        self.key_store = KeyStore()
        self.client_store = ClientStore()
        self.command_context = CommandContext(self.key_store, self.info_store, self.client_store)
        self.master_port = 6379
        self.master_host = "localhost"
        self.__parse_args(args)
        self.slaves = []
        self._init_server_socket()

    def __parse_args(self, args: list):
        host = "localhost"
        port = 6379
        self.is_replica = False
        role = "master"
        if len(args) > 1:
            if args[1] == "--port":
                port = int(args[2])
        self.host: str = host
        self.port: int = port
        if '--replicaof' in args:
            role = 'slave'
            self.is_replica = True
            master_host = args[args.index('--replicaof') + 1]
            master_port = int(args[args.index('--replicaof') + 2])
            print(f"Replicating from {master_host}:{master_port}")
        self.info_store.set("replication", {"role": role, "master_replid": "8371b4fb1155b71f4a04d3e1bc3e18c4a990aeeb",
                                            "master_repl_offset": 0})

    def _init_server_socket(self) -> None:

        self.server: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
        )  # Allow to reuse the same address
        self.server.bind((self.host, self.port))
        if self.is_replica:
            self.connect_to_master()
        print(f"Redis started on {self.host}:{self.port}")

    def handle_client(self, conn: socket.socket, addr: tuple) -> None:
        print(f"[NEW CONNECTION] {addr} connected.")
        command_handler: CommandHandler = CommandHandler(self.command_context)

        connected: bool = True
        while connected:
            msg: bytes = conn.recv(HEADER)
            if not msg or msg == DISCONNECT_MESSAGE:
                connected = False
            else:
                print(f"[{addr}] {msg}")
                data_dict = self.parser.parse(msg)
                command, responses = command_handler.handle_command(
                    data_dict["args"][0], data_dict["args"][1:]
                )
                if isinstance(responses, list):
                    for r in responses:
                        conn.sendall(r)
                        print(r)
                else:
                    conn.sendall(responses)
                    print(responses)
                self.handle_replication(command, msg)
        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected.")

    def handle_replication(self, command, msg):
        if not self.is_replica and len(self.command_context.slaves) > 0 and command == "SET":
            for slave in self.command_context.slaves:
                print("Sending to slave")
                print(msg)
                slave.sendall(msg)

    def connect_to_master(self):
        # Create a TCP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Connect to the server
            client_socket.connect((self.master_host, self.master_port))
            # Send data to the server
            message = "*1\r\n$4\r\nping\r\n"
            client_socket.sendall(message.encode())
            data = client_socket.recv(1024)
            print("Received:", data.decode())
            message = f"*3\r\n$8\r\nREPLCONF\r\n$14\r\nlistening-port\r\n$4\r\n{self.port}\r\n"
            client_socket.sendall(message.encode())
            data = client_socket.recv(1024)
            print("Received:", data.decode())
            message = "*3\r\n$8\r\nREPLCONF\r\n$4\r\ncapa\r\n$6\r\npsync2\r\n"
            client_socket.sendall(message.encode())
            data = client_socket.recv(1024)
            print("Received:", data.decode())
            message = "*3\r\n$5\r\nPSYNC\r\n$1\r\n?\r\n$2\r\n-1\r\n"
            client_socket.sendall(message.encode())
            data = client_socket.recv(4096)
            print("Received:", data)
        except Exception as e:
            print("Error:", e)
        finally:
            # Close the socket
            client_socket.close()

    def start(self) -> None:
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.port}")
        while True:
            conn: socket.socket
            addr: tuple
            conn, addr = self.server.accept()
            thread: threading.Thread = threading.Thread(
                target=self.handle_client, args=(conn, addr)
            )
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

    async def stop(self):
        self.server.shutdown(socket.SHUT_RDWR)
        self.server.close()
