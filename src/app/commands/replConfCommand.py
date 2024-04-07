import socket

from src.app.commands.command import Command
from src.app.commands.commandContext import CommandContext


class ReplConfCommand(Command):
    def execute(self, args: list, command_context: CommandContext) -> bytes:
        repl_command = args[0]
        repl_args = args[1]
        upper_command = repl_command.upper()
        # if upper_command == "LISTENING-PORT":
        #     self.__connect_client(command_context, int(repl_args))
        return b"+OK\r\n"

    def __connect_client(self, command_context, port):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Connect to the server
            print("Connecting to the server", port)
            client_socket.connect(("localhost", port))
            command_context.slaves.append(client_socket)
        except Exception as e:
            print("Error:", e)
