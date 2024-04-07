from src.app.commands.command import Command
from src.app.commands.commandContext import CommandContext


class PingCommand(Command):
    def execute(self, args: list,command_context: CommandContext) -> bytes:
        return b"+PONG\r\n"
