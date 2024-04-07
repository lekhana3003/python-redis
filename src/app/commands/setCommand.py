from src.app.commands.command import Command
import time

from src.app.commands.commandContext import CommandContext


class SetCommand(Command):
    def execute(self, args: dict, command_context: CommandContext) -> bytes:
        expiry_set = False
        key = args[0]
        value = args[1]
        px_syntax = ""
        for i in args:
            if i.upper() == "PX":
                px_syntax = i
                expiry_set = True
        if expiry_set:
            ttl = int(args[args.index(px_syntax) + 1])
            expiry = time.time() * 1000 + ttl
            command_context.key_store.set(key, value, expiry)

        else:
            command_context.key_store.set(key, value)

        return b"+OK\r\n"
