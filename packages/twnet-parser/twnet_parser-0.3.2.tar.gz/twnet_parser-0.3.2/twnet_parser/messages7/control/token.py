from twnet_parser.pretty_print import PrettyPrint

class CtrlToken(PrettyPrint):
    def __init__(
            self,
            response_token: bytes = b'\xff\xff\xff\xff'
    ) -> None:
        self.message_name = 'token'
        self.response_token: bytes = response_token

    def unpack(self, data: bytes, we_are_a_client: bool = False) -> bool:
        if not we_are_a_client:
            # anti reflection attack
            if len(data) < 512:
                return False
        self.response_token = data[0:4]
        return True

    def pack(self, we_are_a_client: bool = True) -> bytes:
        if we_are_a_client:
            return self.response_token + bytes(508)
        return self.response_token
