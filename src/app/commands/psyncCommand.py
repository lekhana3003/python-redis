from src.app.commands.command import Command
from src.app.commands.commandContext import CommandContext

import base64


class PsyncCommand(Command):
    def execute(self, args: list, command_context: CommandContext) -> list:
        message = f'+FULLRESYNC {command_context.info_store.get("replication")["master_replid"]} {command_context.info_store.get("replication")["master_repl_offset"]}\r\n'
        rdb = "UkVESVMwMDEx+glyZWRpcy12ZXIFNy4yLjD6CnJlZGlzLWJpdHPAQPoFY3RpbWXCbQi8ZfoIdXNlZC1tZW3CsMQQAPoIYW9mLWJhc2XAAP/wbjv+wP9aog=="
        binary_data = base64.b64decode(rdb)
        print(binary_data)
        message2 = b"$" + str(len(binary_data)).encode() + b"\r\n" + binary_data
        print(message2)
        return [message.encode(), message2]
