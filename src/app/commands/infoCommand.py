from src.app.commands.command import Command
from src.app.commands.commandContext import CommandContext


class InfoCommand(Command):
    def execute(self, args: list, command_context: CommandContext) -> bytes:
        final_message = ""
        for key in command_context.info_store.get("replication").keys():
            value = str(command_context.info_store.get("replication")[key])
            final_message += f"{key}:{value}\r\n"
        return f"${len(final_message)}\r\n{final_message}\r\n".encode()
