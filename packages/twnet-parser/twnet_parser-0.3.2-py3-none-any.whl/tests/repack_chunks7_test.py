from twnet_parser.packet import *

from twnet_parser.messages7.system.map_change import MsgMapChange

def test_repack_map_change7_chunk() -> None:
    msg = MsgMapChange()
    msg.unpack(
            b'BlmapChill\x00' \
            b'\xde\xcf\xaa\xee\x0b' \
            b'\x8b\xbe\x8a\x01' \
            b'\x08' \
            b'\xa8\x15' \
            b'\x81\x7d\xbf\x48\xc5\xf1\x94\x37\xc4\x58\x2c\x6f\x98\xc9\xc2\x04' \
            b'\xc1\xf1\x69\x76\x32\xf0\x44\x58\x74\x54\x55\x89\x84\x00\xfb\x28')

    assert msg.message_name == 'map_change'

    assert msg.name == 'BlmapChill'
    assert msg.crc == -1592087519
    assert msg.size == 1134475
    assert msg.num_response_chunks_per_request == 8
    assert msg.chunk_size == 1384
    assert msg.sha256 == b'\x81\x7d\xbf\x48\xc5\xf1\x94\x37\xc4' \
                         b'\x58\x2c\x6f\x98\xc9\xc2\x04\xc1\xf1' \
                         b'\x69\x76\x32\xf0\x44\x58\x74\x54\x55' \
                         b'\x89\x84\x00\xfb\x28'

    # change msg and repack to bytes
    msg.name = 'dm1'
    data: bytes = msg.pack()

    # unpack bytes to new message and
    # check if the field updated
    msg_dm1 = MsgMapChange()
    msg_dm1.unpack(data)
    assert msg_dm1.name == 'dm1'

def test_build_map_change7_chunk() -> None:
    msg = MsgMapChange(
            name='BlmapChill',
            crc=-1592087519,
            size=1134475,
            num_response_chunks_per_request=8,
            chunk_size=1384,
            sha256=b'\x81\x7d\xbf\x48\xc5\xf1\x94\x37\xc4' \
                   b'\x58\x2c\x6f\x98\xc9\xc2\x04\xc1\xf1' \
                   b'\x69\x76\x32\xf0\x44\x58\x74\x54\x55' \
                   b'\x89\x84\x00\xfb\x28'
    )

    map_msg_raw = b'BlmapChill\x00' \
                  b'\xde\xcf\xaa\xee\x0b' \
                  b'\x8b\xbe\x8a\x01' \
                  b'\x08' \
                  b'\xa8\x15' \
                  b'\x81\x7d\xbf\x48\xc5\xf1\x94\x37\xc4\x58\x2c\x6f\x98\xc9\xc2\x04' \
                  b'\xc1\xf1\x69\x76\x32\xf0\x44\x58\x74\x54\x55\x89\x84\x00\xfb\x28'

    assert msg.pack() == map_msg_raw

def test_build_ctf5_map_change7_chunk() -> None:
    msg = MsgMapChange(
            name='ctf5',
            crc=-1592087519,
            size=1134475,
            num_response_chunks_per_request=6,
            chunk_size=1384,
            sha256=b'\x81\x7d\xbf\x48\xc5\xf1\x94\x37\xc4' \
                   b'\x58\x2c\x6f\x98\xc9\xc2\x04\xc1\xf1' \
                   b'\x69\x76\x32\xf0\x44\x58\x74\x54\x55' \
                   b'\x89\x84\x00\xfb\x28'
    )

    map_msg_raw = b'ctf5\x00' \
                  b'\xde\xcf\xaa\xee\x0b' \
                  b'\x8b\xbe\x8a\x01' \
                  b'\x06' \
                  b'\xa8\x15' \
                  b'\x81\x7d\xbf\x48\xc5\xf1\x94\x37\xc4\x58\x2c\x6f\x98\xc9\xc2\x04' \
                  b'\xc1\xf1\x69\x76\x32\xf0\x44\x58\x74\x54\x55\x89\x84\x00\xfb\x28'

    assert msg.pack() == map_msg_raw
