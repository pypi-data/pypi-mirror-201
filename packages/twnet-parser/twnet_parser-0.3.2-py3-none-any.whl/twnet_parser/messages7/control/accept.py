from twnet_parser.pretty_print import PrettyPrint

class CtrlAccept(PrettyPrint):
    def __init__(self) -> None:
        self.message_name = 'accept'

    def unpack(self, data: bytes, we_are_a_client: bool = False) -> bool:
        return False

    def pack(self, client: bool = True) -> bytes:
        return b''
