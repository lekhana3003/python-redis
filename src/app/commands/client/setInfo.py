from src.app.commands.command import Command
from src.app.commands.commandContext import CommandContext


class SetInfoCommand(Command):
    def execute(self, args: dict, command_context: CommandContext) -> bytes:
        key = args[0]
        value = args[1]

        command_context.client_store.set(key, value)
        return b"+OK\r\n"