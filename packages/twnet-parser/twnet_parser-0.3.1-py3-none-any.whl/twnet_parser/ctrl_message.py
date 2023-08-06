from typing import Protocol

class CtrlMessage(Protocol):
    message_name: str
    def unpack(self, data: bytes, we_are_a_client: bool = False) -> bool:
        ...
    def pack(self) -> bytes:
        ...
