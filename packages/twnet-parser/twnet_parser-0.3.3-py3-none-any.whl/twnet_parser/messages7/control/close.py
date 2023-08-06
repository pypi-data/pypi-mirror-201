from typing import Optional

from twnet_parser.pretty_print import PrettyPrint
from twnet_parser.packer import Unpacker
from twnet_parser.packer import pack_str

class CtrlClose(PrettyPrint):
    def __init__(
            self,
            reason: Optional[str] = None
    ) -> None:
        self.message_name = 'close'
        self.reason: Optional[str] = reason

    # first byte of data
    # has to be the first byte of the message payload
    # NOT the chunk header and NOT the message id
    def unpack(self, data: bytes, we_are_a_client: bool = False) -> bool:
        unpacker = Unpacker(data)
        self.reason = unpacker.get_str() # TODO: this is an optional field
        return True

    def pack(self) -> bytes:
        if self.reason:
            return pack_str(self.reason)
        return b''
