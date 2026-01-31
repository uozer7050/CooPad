import struct
import time
from dataclasses import dataclass

PACKET_FMT = '<B I H H B B h h h h Q'  # matches protocol.md
PACKET_SIZE = struct.calcsize(PACKET_FMT)
PROTOCOL_VERSION = 2


@dataclass
class GamepadState:
    version: int
    client_id: int
    sequence: int
    buttons: int
    lt: int
    rt: int
    lx: int
    ly: int
    rx: int
    ry: int
    timestamp: int


def pack(state: GamepadState) -> bytes:
    return struct.pack(
        PACKET_FMT,
        state.version,
        state.client_id,
        state.sequence,
        state.buttons,
        state.lt,
        state.rt,
        state.lx,
        state.ly,
        state.rx,
        state.ry,
        state.timestamp,
    )


def unpack(data: bytes) -> GamepadState:
    if len(data) < PACKET_SIZE:
        raise ValueError('packet too small')
    vals = struct.unpack(PACKET_FMT, data[:PACKET_SIZE])
    return GamepadState(*vals)


def make_state_from_inputs(client_id: int, seq: int, buttons: int, lt: int, rt: int, lx: int, ly: int, rx: int, ry: int) -> GamepadState:
    return GamepadState(
        version=PROTOCOL_VERSION,
        client_id=client_id,
        sequence=seq & 0xFFFF,
        buttons=buttons & 0xFFFF,
        lt=lt & 0xFF,
        rt=rt & 0xFF,
        lx=int(lx),
        ly=int(ly),
        rx=int(rx),
        ry=int(ry),
        timestamp=time.perf_counter_ns(),
    )
