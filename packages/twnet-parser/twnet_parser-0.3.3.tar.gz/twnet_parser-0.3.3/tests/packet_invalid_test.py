from twnet_parser.packet import *

def test_parse_7_close():
    # ctrl close 0.7 with last two bytes cut off
    # the last byte of the token and the message id
    # is missing
    try:
        parse7(b'\x04\x0a\x00\xcf\x2e\xde')
    except IndexError:
        #     def parse7(self, data: bytes) -> TwPacket:
        #         pck = TwPacket()
        #         pck.version = '0.7'
        #         pck.header = PacketHeaderParser().parse_header(data)
        #         if pck.header.flags.control:
        # >           if data[7] == 0x04: # close
        # E           IndexError: index out of range
        pass

    # TODO: think of what we want to do here
    #       crash?
    #       silent skip?
    #       detailed error message?
    #       set error field on the packet?
    #       would the error checking be on by default or opt in?
    #       it can affect performance
    #       and a python crash is also pretty informative already
    # assert packet.version == 'unknown'
