from twnet_parser.packer import *

def test_unpack_ints_and_strings() -> None:
    u = Unpacker(b'\x01\x02\x03\x01foo\x00bar\x00')
    assert u.get_int() == 1
    assert u.get_int() == 2
    assert u.get_int() == 3
    assert u.get_int() == 1
    assert u.get_str() == 'foo'
    assert u.get_str() == 'bar'

def test_simple_repack() -> None:
    data: bytes = pack_str('hello world')
    assert data == b'hello world\x00'
    data += pack_int(22)

    u = Unpacker(data)
    assert u.get_str() == 'hello world'
    assert u.get_int() == 22

def test_non_ascii_repack() -> None:
    data: bytes = pack_str('💩')
    assert data == '💩'.encode('utf-8') + b'\x00'

    u = Unpacker(data)
    assert u.get_str() == '💩'

def test_raw_repack_at_end() -> None:
    data: bytes = b''
    data += pack_int(1)
    data += pack_str('a')
    data += b'rawr'

    u = Unpacker(data)
    assert u.get_int() == 1
    assert u.get_str() == 'a'
    assert u.get_raw() == b'rawr'

def test_raw_sized_repack() -> None:
    data: bytes = b''
    data += pack_int(1)
    data += pack_str('a')
    data += b'rawr'
    data += b'abc'
    data += b'\x00\x00'
    data += b'\x01\x02'
    data += pack_int(1)
    data += pack_int(2)
    data += b'\x00\x00'

    u = Unpacker(data)
    assert u.get_int() == 1
    assert u.get_str() == 'a'
    assert u.get_raw(4) == b'rawr'
    assert u.get_raw(3) == b'abc'
    assert u.get_raw(2) == b'\x00\x00'
    assert u.get_raw(2) == b'\x01\x02'
    assert u.get_int() == 1
    assert u.get_int() == 2
    assert u.get_raw(2) == b'\x00\x00'

def test_multi_repack() -> None:
    strs: list[str] = [
            'foo',
            'bar',
            'baz',
            '',
            'yeeeeeeeeeeeeeeeeeee' \
            'eeeeeeeeeeeeeeeeeeee' \
            'eeeeeeeeeeeeeeeeeeee' \
            'eeeeeeeeeeeeeeeeeeee' \
            'eeeeeeeeeeeeeeeeeeee' \
            'eeeeeeeeeeeeeeeeeeee' \
            'eeeppiiiiiiiiiiiiiii',
            'a b c d e f',
            'nameless tee',
            '(1)nameless tee',
            '[D](1)nameless t']

    ints: list[int] = [
            0,
            111111111,
            222222222,
            649010,
            -1,
            -19882,
            29299]

    # pack
    data: bytes = b''
    for string in strs:
        data += pack_str(string)
    for num in ints:
        data += pack_int(num)

    # unpack
    u = Unpacker(data)
    for string in strs:
        assert u.get_str() == string
    for num in ints:
        assert u.get_int() == num
