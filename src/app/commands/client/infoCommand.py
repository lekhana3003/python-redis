from src.app.commands.command import Command
from src.app.commands.commandContext import CommandContext


class ClientInfoCommand(Command):
    def execute(self, args: list, command_context: CommandContext) -> bytes:
        final_message = ""
        for key in command_context.client_store.keys():
            value = str(command_context.client_store.get(key))
            final_message += f"{key}:{value}\r\n"
        return f"${len(final_message)}\r\n{final_message}\r\n".encode()
