from twnet_parser.packet import *

def test_parse_7_close_with_reason():
    packet = parse7(b'\x04\x0a\x00\xcf\x2e\xde\x1d\04shutdown\x00') # 0.7 close

    assert packet.version == '0.7'

    assert packet.header.size == 0
    assert packet.header.ack == 10
    assert packet.header.token == b'\xcf.\xde\x1d'
    assert packet.header.num_chunks == 0

    assert packet.header.flags.control is True
    assert packet.header.flags.resend is False
    assert packet.header.flags.compression is False
    assert packet.header.flags.connless is False

    assert packet.messages[0].message_name == 'close'
    assert len(packet.messages) == 1

    assert packet.messages[0].reason == 'shutdown'

