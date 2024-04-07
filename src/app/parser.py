from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Resp:
    type: str
    value: bytes | str | list | int


class Parser:
    def __init__(self):
        self.command = None
        self.args = []

    def parse(self, data: bytes) -> dict:
        """Parse the incoming data to extract the command and arguments."""
        self.command = None
        self.args = []
        lines = data.split(b"\r\n")
        parse_methods = {
            b"*": self._parse_array,
            b"$": self._parse_bulk_string,
            b":": self._parse_integer,
            b"+": self._parse_simple_string,
        }
        if lines[0]:
            parse_method = parse_methods.get(lines[0][:1])
            if parse_method:
                parse_method(lines)
        return {"command": self.command, "args": self.args}

    def _parse_array(self, lines: List[bytes]) -> None:
        num_elements = int(lines[0][1:])  # Get the number of elements in the array
        self.command = "ARRAY"
        self.args = []
        for i in range(
                1, num_elements * 2, 2
        ):  # Step through the array elements, which are in every second line
            if lines[i].startswith(b"$"):
                # If it's a bulk string, parse it and add to args
                _, value = lines[i: i + 2]  # Get length line and value line
                self.args.append(value.decode())

    def _parse_bulk_string(self, lines: List[bytes]) -> None:
        self.command = "BULK_STRING"
        # The second line is the string value
        self.args = lines[1].decode()  # Decode the bulk string

    def _parse_integer(self, lines: List[bytes]) -> None:
        self.command = "INTEGER"
        # The integer value is in the first line after the colon
        self.args = int(lines[0][1:])

    def _parse_simple_string(self, lines: List[bytes]) -> None:
        self.command = "SIMPLE_STRING"
        self.args = lines[0][1:].decode()

