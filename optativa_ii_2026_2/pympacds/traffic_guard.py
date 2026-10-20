"""traffic_guard — descubre analizadores y aplica la política ante alertas.

Run:  python3 traffic_guard.py -c traffic_guard.ini

Política por defecto: registrar la alerta (JSON Lines) con enfriamiento.
No modifica el cortafuegos; el alumno puede añadir esa acción.
"""

from __future__ import annotations

import asyncio
import json
import os
import time

from pympacds.contracts import ServiceContract, dbus_method
from pympacds.dbus import DBusManager
from pympacds.process import ProcessBase

_ANALYZER_IFACE = "TrafficAnalyzer"
_ANALYZER_PATH = "analyzer"


class TrafficGuardContract(ServiceContract):
    iface_name = "TrafficGuard"
    iface_version = "1.0.0"
    iface_provides = ["traffic.policy"]
    iface_requires = ["traffic.analysis"]

    def __init__(self, ifname: str, base: ProcessBase) -> None:
        super().__init__(ifname, base)
        self._require("dbus_guard_status", "dbus_guard_set_threshold")

    @dbus_method()
    def status(self) -> "s":
        return self.base.dbus_guard_status()

    @dbus_method()
    def set_threshold(self, pps: "i") -> "b":
        return self.base.dbus_guard_set_threshold(pps)


class TrafficGuard(ProcessBase):
    def __init__(self) -> None:
        super().__init__(
            name="traffic_guard",
            version="0.2.0",
            description="Alert policy for the traffic pipeline",
        )
        self._analyzers: dict[str, object] = {}
        self._threshold = 50
        self._cooldown = 5.0
        self._last_action = 0.0
        self._last: dict | None = None
        self._alerts = 0
        self._path = "alerts.jsonl"
        self._configured = False

    async def start_dbus(self) -> bool:
        self.bus = DBusManager(
            logger=self.logger,
            busname="traffic_guard",
            bus_prefix=self.bus_prefix,
        )
        self.iface = TrafficGuardContract(f"{self.bus_prefix}.TrafficGuard", self)
        self.bus.add_interface("guard", self.iface)
        await self.bus.start()
        self.logger.info("traffic_guard started: bus=%s", self.bus.busname)
        return True

    def update_tasks(self) -> None:
        if not self._configured:
            self._threshold = max(
                1, self.config["guard"].getint("threshold_pps", fallback=50)
            )
            self._cooldown = self.config["guard"].getfloat("cooldown_s", fallback=5.0)
            self._path = self.config["guard"].get("alerts_path", fallback="alerts.jsonl")
            os.makedirs(os.path.dirname(os.path.abspath(self._path)), exist_ok=True)
            self._configured = True
        if "scanner" not in self.tasklist:
            self.tasklist["scanner"] = asyncio.create_task(self._scan_analyzers(), name="scanner")

    def dbus_guard_status(self) -> str:
        return json.dumps(
            {
                "analyzers": len(self._analyzers),
                "threshold_pps": self._threshold,
                "alerts": self._alerts,
                "last": self._last,
                "policy": "log",
            }
        )

    def dbus_guard_set_threshold(self, pps: int) -> bool:
        if int(pps) < 1:
            return False
        self._threshold = int(pps)
        self.logger.info("threshold updated: %d pps", self._threshold)
        return True

    def _on_alert(self, proto: str, pps: int) -> None:
        now = time.time()
        if int(pps) < self._threshold or now - self._last_action < self._cooldown:
            return
        self._record(
            {"ts": now, "proto": proto, "pps": int(pps), "action": "log"}
        )
        self.logger.warning("alert recorded: proto=%s pps=%d", proto, pps)

    def _record(self, record: dict) -> None:
        with open(self._path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record) + "\n")
        self._alerts += 1
        self._last = record
        self._last_action = time.time()

    async def _scan_analyzers(self) -> None:
        period = self.config["guard"].getfloat("scan_s", fallback=5.0)
        ifname = f"{self.bus_prefix}.{_ANALYZER_IFACE}"
        objpath = f"{self.bus._obj_root}/{_ANALYZER_PATH}"
        try:
            while not self.exitevent.is_set():
                await self.bus.update_friendbus()
                names = self.bus.query_friend_busname("traffic_analyzer")
                for name in names:
                    if name in self._analyzers:
                        continue
                    try:
                        proxy = await self.bus.get_friend_bus(
                            name, ifname=ifname, objpath=objpath
                        )
                        proxy.on_alert(self._on_alert)
                        self._analyzers[name] = proxy
                        self.logger.info("subscribed to %s", name)
                    except Exception:
                        self.logger.exception("cannot subscribe to %s", name)
                for name in list(self._analyzers):
                    if name not in names:
                        del self._analyzers[name]
                        self.logger.info("unsubscribed from %s", name)
                await self.do_waitexit(timeout=period)
        except asyncio.CancelledError:
            pass


def main() -> None:
    TrafficGuard().start()


if __name__ == "__main__":
    main()
