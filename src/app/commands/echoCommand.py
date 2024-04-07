from src.app.commands.command import Command
from src.app.commands.commandContext import CommandContext



class EchoCommand(Command):
    def execute(self, args: list, command_context: CommandContext) -> bytes:
        message = args[0] if args else ""
        return f"${len(message)}\r\n{message}\r\n".encode()
