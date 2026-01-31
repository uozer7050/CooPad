import threading
import time
import random
from typing import Callable, Optional


class BaseRunner:
    def __init__(self, status_cb: Callable[[str], None], telemetry_cb: Callable[[str], None]):
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self.status_cb = status_cb
        self.telemetry_cb = telemetry_cb

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=1.0)

    def _run(self):
        raise NotImplementedError()


class DummyHost(BaseRunner):
    def _run(self):
        self.status_cb("Host: starting (dummy)")
        seq = 0
        while not self._stop_event.is_set():
            time.sleep(0.5)
            latency = random.uniform(1.0, 8.0)
            self.telemetry_cb(f"Latency: {latency:.1f} ms | seq={seq}")
            seq = (seq + 1) & 0xFFFF
        self.status_cb("Host: stopped")


class DummyClient(BaseRunner):
    def _run(self):
        self.status_cb("Client: starting (dummy)")
        seq = 0
        while not self._stop_event.is_set():
            time.sleep(0.25)
            latency = random.uniform(0.5, 6.0)
            self.telemetry_cb(f"Sent seq={seq} | rtt~{latency:.1f} ms")
            seq = (seq + 1) & 0xFFFF
        self.status_cb("Client: stopped")


def _try_import_real():
    try:
        from gp.core.host import GamepadHost  # type: ignore
        from gp.core.client import GamepadClient  # type: ignore
        return GamepadHost, GamepadClient
    except Exception:
        return None, None


class GpController:
    def __init__(self, status_cb: Callable[[str], None], telemetry_cb: Callable[[str], None]):
        self.status_cb = status_cb
        self.telemetry_cb = telemetry_cb
        HostCls, ClientCls = _try_import_real()
        self._host: BaseRunner
        self._client: BaseRunner
        if HostCls is not None and ClientCls is not None:
            # Wrap real classes to conform to start/stop interface
            class RealHost(BaseRunner):
                def _run(inner_self):
                    try:
                        h = HostCls()
                        inner_self.status_cb("Host: real implementation started")
                        h.start()
                        while not inner_self._stop_event.is_set():
                            time.sleep(0.1)
                        h.stop()
                    except Exception as e:
                        inner_self.status_cb(f"Host error: {e}")

            class RealClient(BaseRunner):
                def _run(inner_self):
                    try:
                        c = ClientCls()
                        inner_self.status_cb("Client: real implementation started")
                        c.start()
                        while not inner_self._stop_event.is_set():
                            time.sleep(0.1)
                        c.stop()
                    except Exception as e:
                        inner_self.status_cb(f"Client error: {e}")

            # wrap callbacks to prefix messages with source
            self._host = RealHost(lambda t: status_cb(f"HOST|{t}"), lambda t: telemetry_cb(f"HOST|{t}"))
            self._client = RealClient(lambda t: status_cb(f"CLIENT|{t}"), lambda t: telemetry_cb(f"CLIENT|{t}"))
        else:
            status_cb("gp/ backend not found — using dummy runners")
            self._host = DummyHost(lambda t: status_cb(f"HOST|{t}"), lambda t: telemetry_cb(f"HOST|{t}"))
            self._client = DummyClient(lambda t: status_cb(f"CLIENT|{t}"), lambda t: telemetry_cb(f"CLIENT|{t}"))

    def start_host(self):
        self._host.start()

    def stop_host(self):
        self._host.stop()

    def start_client(self):
        self._client.start()

    def stop_client(self):
        self._client.stop()
