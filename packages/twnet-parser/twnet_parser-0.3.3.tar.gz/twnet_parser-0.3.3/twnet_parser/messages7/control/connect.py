from twnet_parser.pretty_print import PrettyPrint

class CtrlConnect(PrettyPrint):
    def __init__(
            self,
            response_token: bytes = b'\xff\xff\xff\xff'
    ) -> None:
        self.message_name = 'connect'
        self.response_token: bytes = response_token

    def unpack(self, data: bytes, we_are_a_client: bool = False) -> bool:
        # anti reflection attack
        if len(data) < 512:
            return False
        self.response_token = data[0:4]
        return True

    def pack(self) -> bytes:
        return self.response_token + bytes(508)
