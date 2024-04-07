from src.app.commands.client.infoCommand import ClientInfoCommand
from src.app.commands.client.setInfo import SetInfoCommand
from src.app.commands.command import Command
from src.app.commands.commandContext import CommandContext


class ClientCommand(Command):
    def execute(self, args: list, command_context: CommandContext) -> bytes:
        client_command = args[0]
        client_args = args[1:]
        parser = None
        upper_command = client_command.upper()
        if upper_command == "SETINFO":
            parser = SetInfoCommand(request=client_command)
        if upper_command == "INFO":
            parser = ClientInfoCommand(request=client_command)
        return parser.execute(client_args, command_context)
