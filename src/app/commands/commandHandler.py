from src.app.commands.client.clientCommand import ClientCommand
from src.app.commands.commandContext import CommandContext
from src.app.commands.echoCommand import EchoCommand
from src.app.commands.getCommand import GetCommand
from src.app.commands.infoCommand import InfoCommand
from src.app.commands.pingCommand import PingCommand
from src.app.commands.psyncCommand import PsyncCommand
from src.app.commands.replConfCommand import ReplConfCommand
from src.app.commands.setCommand import SetCommand
from src.app.parser import Parser


class CommandHandler:
    def __init__(self, command_context: CommandContext):
        self.parser = Parser()
        self.__values = {}
        self.command_context = command_context

    def handle_command(self, command: str, args):
        upper_command = command.upper()
        if upper_command == "ECHO":
            parsed_command = EchoCommand(request=upper_command)
        elif upper_command == "PING":
            parsed_command = PingCommand(request=upper_command)
        elif upper_command == "SET":
            parsed_command = SetCommand(request=upper_command)
        elif upper_command == "GET":
            parsed_command = GetCommand(request=upper_command)
        elif upper_command == "INFO":
            parsed_command = InfoCommand(request=upper_command)
        elif upper_command == "REPLCONF":
            parsed_command = ReplConfCommand(request=upper_command)
        elif upper_command == "PSYNC":
            parsed_command = PsyncCommand(request=upper_command)
        elif upper_command == "CLIENT":
            parsed_command = ClientCommand(request=upper_command)
        else:
            print(f"Unknown command: {upper_command}")
            return b"-ERR unknown command\r\n", upper_command
        return upper_command, parsed_command.execute(args=args, command_context=self.command_context)
