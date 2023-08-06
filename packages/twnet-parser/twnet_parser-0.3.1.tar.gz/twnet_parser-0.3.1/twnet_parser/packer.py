#!/usr/bin/env python

# Before chaning the current packer code to extend it
# Consider having two packers
#
# One being this one. That is simple and fast.
# Has no state or side effects.
# Does no error checking.
#
# And another one that sanitizes the data
# will throw errors unexpected data
# return the amount of read and written bytes
# and is attached to a class instance that
# keeps track of a state

class Unpacker():
    def __init__(self, data: bytes) -> None:
        self._data = data
        self.idx = 0

    # first byte of the current buffer
    def byte(self) -> int:
        return self._data[self.idx]

    def data(self) -> bytes:
        return self._data[self.idx:]

    def get_raw(self, size: int = -1) -> bytes:
        if size == -1:
            return self.data()
        end: int = self.idx + size
        data: bytes = self._data[self.idx:end]
        self.idx = end
        return data

    def get_int(self) -> int:
        sign = (self.byte() >> 6) & 1
        res = self.byte() & 0x3F
        # fake loop should only loop once
        # its the poor mans goto hack
        while True:
            if (self.byte() & 0x80) == 0:
                break
            self.idx += 1
            res |= (self.byte() & 0x7F) << 6

            if (self.byte() & 0x80) == 0:
                break
            self.idx += 1
            res |= (self.byte() & 0x7F) << (6 + 7)

            if (self.byte() & 0x80) == 0:
                break
            self.idx += 1
            res |= (self.byte() & 0x7F) << (6 + 7 + 7)

            if (self.byte() & 0x80) == 0:
                break
            self.idx += 1
            res |= (self.byte() & 0x7F) << (6 + 7 + 7 + 7)
            break

        self.idx += 1
        res ^= -sign
        return res

    def get_str(self) -> str:
        str_end: int = self.data().find(b'\x00')
        res: bytes = self.data()[:str_end]
        self.idx += str_end + 1
        # TODO: add saitize and sanitize cc
        return res.decode('utf-8')

# TODO: optimize performance and benchmark in tests
def pack_int(num: int) -> bytes:
    res: bytearray = bytearray(b'\x00')
    if num < 0:
        res[0] |= 0x40 # set sign bit
        num = ~num

    res[0] |= num & 0x3F # pack 6bit into res
    num >>= 6 # discard 6 bits

    i = 0
    while num != 0:
        res[i] |= 0x80 # set extend bit
        i += 1
        res.extend(bytes([num & 0x7F])) # pack 7 bit
        num >>= 7 # discard 7 bits
    return bytes(res)

def pack_str(data: str) -> bytes:
    return data.encode('utf-8') + b'\x00'

# TODO: optimize performance and benchmark in tests
def unpack_int(data: bytes) -> int:
    sign = (data[0] >> 6) & 1
    res = data[0] & 0x3F
    i = 0
    # fake loop should only loop once
    # its the poor mans goto hack
    while True:
        if (data[i] & 0x80) == 0:
            break
        i += 1
        res |= (data[i] & 0x7F) << 6

        if (data[i] & 0x80) == 0:
            break
        i += 1
        res |= (data[i] & 0x7F) << (6 + 7)

        if (data[i] & 0x80) == 0:
            break
        i += 1
        res |= (data[i] & 0x7F) << (6 + 7 + 7)

        if (data[i] & 0x80) == 0:
            break
        i += 1
        res |= (data[i] & 0x7F) << (6 + 7 + 7 + 7)
        break

    res ^= -sign
    return res
