from twnet_parser.packer import *

def test_pack_small_positive_ints():
    assert pack_int(1) == b'\x01'
    assert pack_int(2) == b'\x02'
    assert pack_int(3) == b'\x03'

    assert pack_int(44) == b'\x2C'
    assert pack_int(45) == b'\x2D'
    assert pack_int(46) == b'\x2E'

def test_pack_multi_byte_positive_ints():
    assert pack_int(63) == b'\x3F'
    assert pack_int(64) == b'\x80\x01'
    assert pack_int(65) == b'\x81\x01'

def test_pack_small_negative_ints():
    assert pack_int(-1) == b'\x40'
    assert pack_int(-2) == b'\x41'
    assert pack_int(-3) == b'\x42'

    assert pack_int(-44) == b'\x6B'
    assert pack_int(-45) == b'\x6C'
    assert pack_int(-46) == b'\x6D'

def test_pack_multi_byte_negative_ints():
    assert pack_int(-63) == b'\x7E'
    assert pack_int(-64) == b'\x7F'
    assert pack_int(-65) == b'\xC0\x01'

def test_pack_multi_byte_positive_and_negative():
    assert pack_int(-66663) == b'\xe6\x91\x08'
    assert pack_int(66663) == b'\xa7\x91\x08'

    assert pack_int(-8866663) == b'\xe6\xad\xba\x08'
    assert pack_int(8866663) == b'\xa7\xad\xba\x08'

# TODO: should we just pack numbers bigger than 4 bytes?
#       since the official tw client and server are written in C++
#       they do not support such big numbers
#       we could also throw an error here instead
def test_pack_too_big_positive_and_negative():
    assert pack_int(-98866996963) == b'\xe2\x9b\xf5\xce\xe0\x05'
    assert pack_int(98866996963) == b'\xa3\x9b\xf5\xce\xe0\x05'

def test_unpack_small_positive_ints():
    assert unpack_int(b'\x01') == 1
    assert unpack_int(b'\x02') == 2
    assert unpack_int(b'\x03') == 3

def test_unpack_multi_byte_positive_ints():
    assert unpack_int(b'\x3F') == 63
    assert unpack_int(b'\x80\x01') == 64
    assert unpack_int(b'\x81\x01') == 65

def test_unpack_only_first_int():
    assert unpack_int(b'\x01\x01') == 1
    #                    ^
    #       should only read this byte

    assert unpack_int(bytes([0b00000001])) == 1
    #                          ESDDDDDD

    assert unpack_int(bytes([0b00000001, 0b00000001])) == 1
    #                          ESDDDDDD    ESDDDDDD
    #                          ^
    #                      not extended
    #                      ignore next byte

    assert unpack_int(bytes([0b01000010, 0b11111111])) == -3
    #                          ESDDDDDD    ESDDDDDD
    #                          ^^          ^      ^
    #                          ||          \______/
    #                          ||             |
    #                          ||          should all be ignored by the unpacker
    #                          ||
    #                          ||
    #                          |sign bit -> negative
    #                          |
    #                      not extended
    #                      ignore next byte

def test_repacked_ints_should_match():
    for i in range(-127, 128):
        assert i == unpack_int(pack_int(i))
    for i in range(512, 1024):
        assert i == unpack_int(pack_int(i))
    for i in range(-512, -1024):
        assert i == unpack_int(pack_int(i))

def test_multi_byte_repacked_ints_should_match():
    for i in range(8_000, 8_500):
        assert i == unpack_int(pack_int(i))
    for i in range(-8_000, 8_500):
        assert i == unpack_int(pack_int(i))
    for i in range(-9_900, 10_100):
        assert i == unpack_int(pack_int(i))

def test_big_repacked_ints_should_match():
    for i in [
            99_000,
            -99_000,
            500_000,
            -500_000,
            900_000,
            -900_000,
            99_999_999,
            -99_999_999,
            999_999_999_999_999
            -999_999_999_999_999]:
        assert i == unpack_int(pack_int(i))

