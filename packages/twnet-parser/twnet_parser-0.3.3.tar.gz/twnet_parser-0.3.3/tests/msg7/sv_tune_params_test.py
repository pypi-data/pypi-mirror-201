from twnet_parser.messages7.game.sv_tune_params import MsgSvTuneParams

def test_tune_repack_custom_gravity() -> None:
    # chunk header: b'A\x86\x82\x0c'
    data = \
        b'\xa8\x0f\x88\x032\xa8\x14\xb0\x12\xb4\x07\x96\x02' \
        b'\x9f\x01\xb0\xd1\x04\x80}\xac\x04\x9c\x17\x90\x1f\x98\xdb\x06' \
        b'\x80\xb5\x18\x8c\x02\xbd\x01\xa0\xed\x1a\x88\x03\xbd\x01\xb8' \
        b'\xc8!\x90\x01\x14\xbc\n\xa0\x9a\x0c\x88\x03\x80\xe2\t' \
        b'\x98\xea\x01\xa4\x01\x00\xa4\x01\xa4\x01'

    tune = MsgSvTuneParams()
    tune.unpack(data)

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

    repack = tune.pack()

    assert repack == data

def test_change_values() -> None:
    tune = MsgSvTuneParams()
    tune.ground_control_speed = 400
    tune.gravity = 0.25
    data = tune.pack()

    new_tune = MsgSvTuneParams()
    new_tune.unpack(data)
    assert new_tune.ground_control_speed == 400
    assert new_tune.gravity == 0.25

def test_defaults() -> None:
    tune = MsgSvTuneParams()

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
    assert tune.gravity == 0.5
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

def test_tune_reset() -> None:
    # chunk header: b'\x41\x85\xbc\x0c'
    data = \
        b'\xa8\x0f\x88\x03\x32\xa8\x14' \
        b'\xb0\x12\xb4\x07\x96\x02\x9f' \
        b'\x01\xb0\xd1\x04\x80\x7d\xac' \
        b'\x04\x9c\x17\x32\x98\xdb\x06' \
        b'\x80\xb5\x18\x8c\x02\xbd\x01' \
        b'\xa0\xed\x1a\x88\x03\xbd\x01' \
        b'\xb8\xc8\x21\x90\x01\x14\xbc' \
        b'\x0a\xa0\x9a\x0c\x88\x03\x80' \
        b'\xe2\x09\x98\xea\x01\xa4\x01' \
        b'\x00\xa4\x01\xa4\x01'

    tune = MsgSvTuneParams()
    tune.unpack(data)

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
    assert tune.gravity == 0.5
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

    repack = tune.pack()

    assert repack == data
