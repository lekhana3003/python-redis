from src.app.commands.command import Command

from src.app.commands.commandContext import CommandContext


class GetCommand(Command):
    def execute(self, args: dict, command_context: CommandContext) -> bytes:
        key = args[0]
        values = command_context.key_store.get(key)
        if values is None:
            return b"$-1\r\n"
        value = values[0]
        return f"${len(value)}\r\n{value}\r\n".encode()
