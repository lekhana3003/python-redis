from abc import ABC, abstractmethod

from src.app.commands.commandContext import CommandContext



class Command(ABC):
    def __init__(self, request: str) -> None:
        super().__init__()
        self.request = request

    @abstractmethod
    def execute(self, args: list, command_context: CommandContext) -> bytes:
        pass
