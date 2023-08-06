from twnet_parser.pretty_print import PrettyPrint

class CtrlKeepAlive(PrettyPrint):
    def __init__(self) -> None:
        self.message_name = 'keep_alive'

    def unpack(self, data: bytes, we_are_a_client: bool = False) -> bool:
        return False

    def pack(self) -> bytes:
        return b''
