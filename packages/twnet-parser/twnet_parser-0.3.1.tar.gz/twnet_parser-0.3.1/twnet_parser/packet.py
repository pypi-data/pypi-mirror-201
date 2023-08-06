#!/usr/bin/env python

from typing import Union
from typing import cast

from twnet_parser import packer
from twnet_parser.pretty_print import PrettyPrint
from twnet_parser.message_parser import MessageParser
from twnet_parser.net_message import NetMessage
from twnet_parser.ctrl_message import CtrlMessage
from twnet_parser.chunk_header import ChunkHeader, ChunkFlags
from twnet_parser.msg_matcher.control7 import match_control7

from twnet_parser.external.huffman import huffman

# TODO: what is a nice pythonic way of storing those?
#       also does some version:: namespace thing make sense?
PACKETFLAG7_CONTROL = 1
PACKETFLAG7_RESEND = 2
PACKETFLAG7_COMPRESSION = 4
PACKETFLAG7_CONNLESS = 8

CHUNKFLAG7_VITAL = 1
CHUNKFLAG7_RESEND = 2

PACKET_HEADER7_SIZE = 7

class PacketFlags7(PrettyPrint):
    def __init__(self):
        self.control = False
        self.resend = False
        self.compression = False
        self.connless = False

class PacketFlags6(PrettyPrint):
    def __init__(self):
        self.token = False
        self.control = False
        self.resend = False
        self.compression = False
        self.connless = False

class PacketHeader(PrettyPrint):
    def __init__(self) -> None:
        self.flags: PacketFlags7 = PacketFlags7()
        self.size: int = 0
        self.ack: int = 0
        self.token: bytes = b'\xff\xff\xff\xff'
        self.num_chunks: int = 0

class TwPacket(PrettyPrint):
    def __init__(self) -> None:
        self.version: str = 'unknown'
        self.payload_raw: bytes = b''
        self.payload_decompressed: bytes = b''
        self.header: PacketHeader = PacketHeader()
        self.messages: list[Union[CtrlMessage, NetMessage]] = []

class PacketHeaderParser7():
    def parse_flags7(self, data: bytes) -> PacketFlags7:
        # FFFF FFaa
        flag_bits = (data[0] & 0xfc) >> 2
        flags = PacketFlags7()
        flags.control = (flag_bits & PACKETFLAG7_CONTROL) != 0
        flags.resend = (flag_bits & PACKETFLAG7_RESEND) != 0
        flags.compression = (flag_bits & PACKETFLAG7_COMPRESSION) != 0
        flags.connless = (flag_bits & PACKETFLAG7_CONNLESS) != 0
        return flags

    def parse_ack(self, header_bytes: bytes) -> int:
        # ffAA AAAA AAAA
        return ((header_bytes[0] & 0x3) << 8) | header_bytes[1]

    def parse_num_chunks(self, header_bytes: bytes) -> int:
        # TODO: not sure if this is correct
        return header_bytes[2]

    def parse_token(self, header_bytes: bytes) -> bytes:
        return header_bytes[3:7]

    def parse_header(self, data: bytes) -> PacketHeader:
        header = PacketHeader()
        # bits 2..5
        header.flags = self.parse_flags7(data)
        # bits 6..16
        header.ack = self.parse_ack(data)
        # bits 17..25
        header.num_chunks = self.parse_num_chunks(data)
        # bits 16..57
        header.token = self.parse_token(data)
        return header

class ChunkHeaderParser:
    def parse_flags7(self, data: bytes) -> ChunkFlags:
        # FFss ssss  xxss ssss
        flag_bits = (data[0] >> 6) & 0x03
        flags = ChunkFlags()
        flags.resend = (flag_bits & CHUNKFLAG7_RESEND) != 0
        flags.vital = (flag_bits & CHUNKFLAG7_VITAL) != 0
        return flags

    # the first byte of data has to be the
    # first byte of the chunk header
    def parse_header7(self, data: bytes) -> ChunkHeader:
        header = ChunkHeader()
        header.flags = self.parse_flags7(data)
        # ffSS SSSS  xxSS SSSS
        header.size = ((data[0] & 0x3F) << 6) | (data[1] & 0x3F)
        if header.flags.vital:
            # ffss ssss  XXss ssss
            header.seq = ((data[1] & 0xC0) << 2) | data[2]
        return header

class PacketParser():
    # the first byte of data has to be the
    # first byte of a message chunk
    # NOT the whole packet with packet header
    def get_messages(self, data: bytes) -> list[NetMessage]:
        messages: list[NetMessage] = []
        i = 0
        while i < len(data):
            msg = self.get_message(data[i:])
            i += msg.header.size + 2 # header + msg id = 3
            if msg.header.flags.vital:
                i += 1
            messages.append(msg)
        return messages

    # the first byte of data has to be the
    # first byte of a message chunk
    # NOT the whole packet with packet header
    def get_message(self, data: bytes) -> NetMessage:
        chunk_header = ChunkHeaderParser().parse_header7(data)
        i = 2
        if chunk_header.flags.vital:
            i += 1
        msg_id: int = packer.unpack_int(data[i:])
        i += 1
        sys: bool = (msg_id & 1) == 1
        msg_id >>= 1
        msg: NetMessage
        if sys:
            msg = MessageParser().parse_sys_message(msg_id, data[i:])
        else:
            msg = MessageParser().parse_game_message(msg_id, data[i:])
        msg.header = chunk_header
        return msg

    def parse7(self, data: bytes, client: bool) -> TwPacket:
        pck = TwPacket()
        pck.version = '0.7'
        # TODO: what is the most performant way in python to do this?
        #       heap allocating a PacketHeaderParser7 just to bundle a bunch of
        #       methods that do not share state seems like a waste of performance
        #       would this be nicer with class methods?
        pck.header = PacketHeaderParser7().parse_header(data)
        pck.payload_raw = data[PACKET_HEADER7_SIZE:]
        pck.payload_decompressed = pck.payload_raw
        if pck.header.flags.control:
            ctrl_msg: CtrlMessage = match_control7(data[7], data[8:], client)
            pck.messages.append(ctrl_msg)
            return pck
        if pck.header.flags.compression:
            payload = bytearray(pck.payload_raw)
            pck.payload_decompressed = huffman.decompress(payload)
        pck.messages = cast(
                list[Union[CtrlMessage, NetMessage]],
                self.get_messages(pck.payload_decompressed))
        return pck

def parse6(data: bytes) -> TwPacket:
    raise NotImplementedError()

def parse7(data: bytes, we_are_a_client: bool = False) -> TwPacket:
    return PacketParser().parse7(data, we_are_a_client)
