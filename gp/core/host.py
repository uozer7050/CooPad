import socket
import threading
import time
from typing import Optional

from .protocol import unpack, PROTOCOL_VERSION

try:
    import vgamepad as vg
    VGAME_AVAILABLE = True
except Exception:
    VGAME_AVAILABLE = False


class GamepadHost:
    def __init__(self, bind_ip: str = "", port: int = 7777, status_cb=None):
        self.bind_ip = bind_ip
        self.port = port
        self._sock: Optional[socket.socket] = None
        self._thread: Optional[threading.Thread] = None
        self._stop = threading.Event()
        self._last_seq = None
        self._last_buttons = 0
        self._owner = None
        self._last_time = 0.0
        self.status_cb = status_cb or (lambda s: print(f"HOST: {s}"))
        self._vg = None

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop.set()
        if self._sock:
            try:
                self._sock.close()
            except Exception:
                pass
        if self._thread:
            self._thread.join(timeout=1.0)

    def _run(self):
        self.status_cb('listening on %s:%d' % (self.bind_ip or '*', self.port))
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((self.bind_ip, self.port))
        if VGAME_AVAILABLE:
            try:
                self._vg = vg.VX360Gamepad()
                self.status_cb('vgamepad initialized')
            except Exception as e:
                self.status_cb(f'vgamepad init error: {e}')

        while not self._stop.is_set():
            try:
                self._sock.settimeout(0.5)
                data, addr = self._sock.recvfrom(1024)
            except socket.timeout:
                # check ownership timeout
                if self._owner and (time.time() - self._last_time) > 0.5:
                    self.status_cb('owner timeout, clearing state')
                    self._owner = None
                    self._last_seq = None
                continue
            except Exception as e:
                self.status_cb(f'recv error: {e}')
                continue

            try:
                state = unpack(data)
            except Exception as e:
                self.status_cb(f'bad packet: {e}')
                continue

            if state.version != PROTOCOL_VERSION:
                self.status_cb(f'bad version {state.version} from {addr}')
                continue

            # ownership
            if self._owner is None:
                self._owner = state.client_id
                self.status_cb(f'owner set to {self._owner}')

            if state.client_id != self._owner:
                # ignore others
                continue

            # simple seq check
            if self._last_seq is not None:
                diff = (state.sequence - self._last_seq) & 0xFFFF
                if diff == 0:
                    # duplicate
                    continue
            self._last_seq = state.sequence
            self._last_time = time.time()

            # apply state to vgamepad if available
            try:
                self._apply_state(state)
            except Exception as e:
                self.status_cb(f'apply state error: {e}')

    def _apply_state(self, state):
        # For simplicity, if vgamepad not available just log the state
        if self._vg is None:
            self.status_cb(f'recv seq={state.sequence} bt={state.buttons:#06x} lt={state.lt} rt={state.rt} lx={state.lx} ly={state.ly} rx={state.rx} ry={state.ry}')
            return

        # Full XInput mapping per protocol.md
        try:
            buttons = state.buttons

            # mapping: protocol bits -> vgamepad XUSB_BUTTON enum
            mapping = {
                0x0001: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
                0x0002: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
                0x0004: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
                0x0008: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
                0x0010: vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
                0x0020: vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
                0x0040: vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
                0x0080: vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
                0x0100: vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
                0x0200: vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
                0x1000: vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
                0x2000: vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
                0x4000: vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
                0x8000: vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
            }

            # Press/release based on diff from last_buttons
            for bitmask, btn_enum in mapping.items():
                had = bool(self._last_buttons & bitmask)
                now = bool(buttons & bitmask)
                if now and not had:
                    self._vg.press_button(button=btn_enum)
                elif not now and had:
                    self._vg.release_button(button=btn_enum)

            # update last buttons
            self._last_buttons = buttons

            # axes: vgamepad expects -32768..32767 for sticks
            # ensure values are ints in range
            lx = int(max(-32768, min(32767, state.lx)))
            ly = int(max(-32768, min(32767, state.ly)))
            rx = int(max(-32768, min(32767, state.rx)))
            ry = int(max(-32768, min(32767, state.ry)))
            self._vg.left_joystick(lx, ly)
            self._vg.right_joystick(rx, ry)

            # triggers 0-255 expected
            lt = int(max(0, min(255, state.lt)))
            rt = int(max(0, min(255, state.rt)))
            self._vg.left_trigger(lt)
            self._vg.right_trigger(rt)

            self._vg.update()
        except Exception as e:
            self.status_cb(f'vgamepad apply error: {e}')
