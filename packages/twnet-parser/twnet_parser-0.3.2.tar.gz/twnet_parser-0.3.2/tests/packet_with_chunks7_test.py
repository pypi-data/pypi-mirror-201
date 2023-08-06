from twnet_parser.packet import parse7

def test_parse_7_real_map_change():
    packet = parse7(b'\x00\x01\x01\x58\xeb\x9a\xf4' \
            b'\x40\x38\x01' \
            b'\x05BlmapChill\x00' \
            b'\xde\xcf\xaa\xee\x0b' \
            b'\x8b\xbe\x8a\x01' \
            b'\x08' \
            b'\xa8\x15' \
            b'\x81\x7d\xbf\x48\xc5\xf1\x94\x37\xc4\x58\x2c\x6f\x98\xc9\xc2\x04\xc1\xf1\x69\x76\x32\xf0\x44\x58\x74\x54\x55\x89\x84\x00\xfb\x28')

    assert packet.version == '0.7'

    assert packet.header.token == b'\x58\xeb\x9a\xf4'
    assert packet.header.num_chunks == 1
    assert packet.header.ack == 1

    assert packet.header.flags.control is False
    assert packet.header.flags.compression is False

    # TODO: uncomment
    assert len(packet.messages) == 1
    assert packet.messages[0].message_name == 'map_change'

    # Teeworlds 0.7 Protocol packet
    #     Flags: none (..00 00..)
    #         ..0. .... = Connection-oriented
    #         ...0 .... = Not compressed
    #         .... 0... = No resend requested
    #         .... .0.. = Not a control message
    #     Acknowledged sequence number: 1 (.... ..00 0000 0001)
    #     Number of chunks: 1
    #     Token: 58eb9af4
    #     Payload (59 bytes)
    # Teeworlds 0.7 Protocol chunk: sys.map_change
    #     Header (vital: 1)
    #         Flags: vital (01.. ....)
    #         Size: 56 bytes (..00 0000 ..11 1000)
    #         Sequence number: 1 (00.. .... 0000 0001)
    #     Message: sys.map_change
    #     Name: "BlmapChill"
    #     Crc: -1592087519
    #     Size: 1134475
    #     Num response chunks per request: 8
    #     Chunk size: 1384
    #     Sha256: 817dbf48c5f19437c4582c6f98c9c204c1f1697632f04458745455898400fb28


def test_parse_7_real_multi_chunk_compressed():
    # 0.7 motd, srv settings, ready
    packet = parse7(b'\x10\x02\x03\x58\xeb\x9a\xf4\x4a\x42\x88\x4a\x6e\x16\xba\x31\x46\xa2\x84\x9e\xbf\xe2\x06')
    #                   ^   ^   ^  ^             ^ ^                                                         ^
    #                   |ack=2  |  \_____________/ \_________________________________________________________/
    #                   |       |       |                                  |
    #                   |  chunks=3   token                           huffman compressed
    #                   |                                             3 chunks:
    #              compression=true                       game.sv_motd, game.sv_server_settings, sys.con_ready
    #
    #                                     payload should decompress
    #                                     from: b'\x4a\x42\x88\x4a\x6e\x16\xba\x31\x46\xa2\x84\x9e\xbf\xe2\x06'
    #                                     to:   b'\x40\x02\x02\x02\x00\x40\x07\x03\x22\x01\x00\x01\x00\x01\x08\x40\x01\x04\x0b'
    #                                              ^                 ^ ^                                     ^ ^             ^ 
    #                                              \_________________/ \_____________________________________/ \_____________/
    #                                                     |                       |                                    |
    #                                                 motd                     server_settings                      ready

    assert packet.payload_raw == b'\x4a\x42\x88\x4a\x6e\x16\xba\x31\x46\xa2\x84\x9e\xbf\xe2\x06'
    assert packet.payload_decompressed == b'\x40\x02\x02\x02\x00\x40\x07\x03\x22\x01\x00\x01\x00\x01\x08\x40\x01\x04\x0b'

    # Teeworlds 0.7 Protocol chunk: game.sv_motd
    #     Header (vital: 2)
    #         Flags: vital (01.. ....)
    #         Size: 2 bytes (..00 0000 ..00 0010)
    #         Sequence number: 2 (00.. .... 0000 0010)
    #     Message: game.sv_motd
    #     Message: ""
    # Teeworlds 0.7 Protocol chunk: game.sv_server_settings
    #     Header (vital: 3)
    #         Flags: vital (01.. ....)
    #         Size: 7 bytes (..00 0000 ..00 0111)
    #         Sequence number: 3 (00.. .... 0000 0011)
    #     Message: game.sv_server_settings
    #     Kick vote: true
    #     Kick min: 0
    #     Spec vote: true
    #     Team lock: false
    #     Team balance: true
    #     Player slots: 8
    # Teeworlds 0.7 Protocol chunk: sys.con_ready
    #     Header (vital: 4)
    #         Flags: vital (01.. ....)
    #         Size: 1 byte (..00 0000 ..00 0001)
    #         Sequence number: 4 (00.. .... 0000 0100)
    #     Message: sys.con_ready



    assert packet.version == '0.7'

    assert packet.header.token == b'\x58\xeb\x9a\xf4'

    assert packet.header.num_chunks == 3
    assert packet.header.ack == 2

    assert packet.header.flags.compression is True
    assert packet.header.flags.control is False

    assert len(packet.messages) == 3
    assert packet.messages[0].message_name == 'sv_motd'
    assert packet.messages[1].message_name == 'sv_server_settings'
    assert packet.messages[2].message_name == 'con_ready'

def test_parse_7_real_broadcast_input_snap() -> None:
    # 0.7 packet header
    data: bytes = b'\x00\x07\x03\x4d\xcb\x93\x60'
    # game.sv_broadcast
    data += b'\x40\x8d\x7b\x04\x68\x65\x6c\x6c\x6f\x20\x77\x6f\x72\x6c\x64\x00'
    # sys.input_timing
    data += b'\x00\x04\x15\xbd\x06\x13'
    # sys.snap_empty
    data += b'\x00\x04\x0f\xbe\x06\x04'
    # Teeworlds 0.7 Protocol packet
    #     Flags: none (..00 00..)
    #     Acknowledged sequence number: 7 (.... ..00 0000 0111)
    #     Number of chunks: 3
    #     Token: 4dcb9360
    #     Payload (28 bytes)
    # Teeworlds 0.7 Protocol chunk: game.sv_broadcast
    #     Header (vital: 635)
    #     Message: game.sv_broadcast
    #     Message: "hello world"
    # Teeworlds 0.7 Protocol chunk: sys.input_timing
    #     Header (non-vital)
    #     Message: sys.input_timing
    #     Input pred tick: 445
    #     Time left: 19
    # Teeworlds 0.7 Protocol chunk: sys.snap_empty
    #     Header (non-vital)
    #     Message: sys.snap_empty
    #     Tick: 446
    #     Delta tick: 4

    packet = parse7(data)

    assert len(packet.messages) == 3

    assert packet.messages[0].message_name == 'sv_broadcast'
    assert packet.messages[0].system_message is False

    assert packet.messages[1].message_name == 'input_timing'
    assert packet.messages[1].system_message is True

    assert packet.messages[2].message_name == 'snap_empty'
    assert packet.messages[2].system_message is True

def test_parse_7_real_rcon_and_input() -> None:
    data = b'\x02\x81\x02\x5b\x30\xe5\x81' \
        b'\x40\x11\x09\x2b\x74\x75\x6e\x65\x20\x67\x72\x61\x76\x69\x74\x79\x20\x32\x30\x00' \
        b'\x00\x11\x29\x80\x5a\x83\x5a\x28\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x21'

    packet = parse7(data)

    assert len(packet.messages) == 2

    rcon = packet.messages[0]
    inp = packet.messages[1]

    assert rcon.message_name == 'rcon_cmd'
    assert rcon.cmd == 'tune gravity 20'

    assert inp.message_name == 'input'
    assert inp.ack_snapshot == 5760
    assert inp.intended_tick == 5763
    assert inp.input_size == 40

def test_parse_7_real_tune_params_rcon_line_input_timing_snap_empty() -> None:
    """
    This is a direct response to the packet from

    test_parse_7_real_rcon_and_input()

    copied straight from a packet dump of a vanilla 0.7 server
    talking to a vanilla 0.7 client
    """
    data = b'\x00\t\x04{FN\xb5' \
        b'A\x86\x82\x0c\xa8\x0f\x88\x032\xa8\x14\xb0\x12\xb4\x07\x96\x02' \
        b'\x9f\x01\xb0\xd1\x04\x80}\xac\x04\x9c\x17\x90\x1f\x98\xdb\x06' \
        b'\x80\xb5\x18\x8c\x02\xbd\x01\xa0\xed\x1a\x88\x03\xbd\x01\xb8' \
        b'\xc8!\x90\x01\x14\xbc\n\xa0\x9a\x0c\x88\x03\x80\xe2\t' \
        b'\x98\xea\x01\xa4\x01\x00\xa4\x01\xa4\x01' \
        b'@\xae\x83\x1b[08:52:58][tuning]: gravity changed to 20.00\x00' \
        b'\x00\x04\x15\x83Z\n' \
        b'\x00\x04\x0f\x84Z\x04'

    packet = parse7(data)

    assert len(packet.messages) == 4

    tune = packet.messages[0]
    rcon = packet.messages[1]
    timing = packet.messages[2]
    snap = packet.messages[3]

    assert tune.message_name == 'sv_tune_params'
    assert tune.ground_control_speed == 10
    assert tune.ground_control_accel == 2
    assert tune.ground_friction == 0.5
    assert tune.ground_jump_impulse == 13.2
    assert tune.air_jump_impulse == 12
    assert tune.air_control_speed == 5
    assert tune.air_control_accel == 1.5
    assert tune.air_friction == 0.95
    assert tune.hook_length == 380
    assert tune.hook_fire_speed == 80
    assert tune.hook_drag_accel == 3
    assert tune.hook_drag_speed == 15
    assert tune.gravity == 20
    assert tune.velramp_start == 550
    assert tune.velramp_range == 2000
    assert tune.velramp_curvature == 1.4
    assert tune.gun_curvature == 1.25
    assert tune.gun_speed == 2200
    assert tune.gun_lifetime == 2
    assert tune.shotgun_curvature == 1.25
    assert tune.shotgun_speed == 2750
    assert tune.shotgun_speeddiff == 0.8
    assert tune.shotgun_lifetime == 0.2
    assert tune.grenade_curvature == 7
    assert tune.grenade_speed == 1000
    assert tune.grenade_lifetime == 2
    assert tune.laser_reach == 800
    assert tune.laser_bounce_delay == 150
    assert tune.laser_bounce_num == 1
    assert tune.laser_bounce_cost == 0
    assert tune.player_collision == 1
    assert tune.player_hooking == 1

    assert rcon.message_name == 'rcon_line'
    assert rcon.line == '[08:52:58][tuning]: gravity changed to 20.00'

    assert timing.message_name == 'input_timing'
    assert timing.input_pred_tick == 5763
    assert timing.time_left == 10

    assert snap.message_name == 'snap_empty'
    assert snap.tick == 5764
    assert snap.delta_tick == 4

