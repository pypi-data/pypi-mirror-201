from twnet_parser.packet import *

# TODO: uncomment and adjust ack/size when 0.6 is done

# def test_parse_065_close():
#     packet = parse7(b'\x10\x10\x00\x04\x9a\xcb\x09\xc9') # 0.6.5 close
# 
#     assert packet.version == '0.6.5'
# 
#     assert packet.header.size == 0
#     assert packet.header.ack == 10
#     assert packet.header.token == b'\x9a\xcb\x09\xc9'
#     assert packet.header.num_chunks == 0
# 
#     assert packet.header.flags.control == True
#     assert packet.header.flags.resend == False
#     assert packet.header.flags.compression == False
#     assert packet.header.flags.connless == False
# 
#     assert packet.messages[0].message_name == 'close'
#     assert len(packet.messages) == 1
