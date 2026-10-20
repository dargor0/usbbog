"""traffic_analyzer — descubre sensores, agrega paquetes y emite alertas.

Run:  python3 traffic_analyzer.py -c traffic_analyzer.ini

No captura tráfico: se suscribe a la señal ``packet`` de cada
``traffic_sensor`` descubierto en el mismo ``bus_prefix``.
"""

from __future__ import annotations

import asyncio
import json
import time

from pympacds.contracts import ServiceContract, dbus_method, dbus_signal
from pympacds.dbus import DBusManager
from pympacds.process import ProcessBase

from traffic_common import Window, flow_key

_SENSOR_IFACE = "TrafficSensor"
_SENSOR_PATH = "traffic"


class TrafficAnalyzerContract(ServiceContract):
    iface_name = "TrafficAnalyzer"
    iface_version = "1.0.0"
    iface_provides = ["traffic.analysis"]
    iface_requires = ["traffic.capture"]

    def __init__(self, ifname: str, base: ProcessBase) -> None:
        super().__init__(ifname, base)
        self._require("dbus_analyzer_summary", "dbus_analyzer_top_flows")

    @dbus_method()
    def summary(self) -> "s":
        return self.base.dbus_analyzer_summary()

    @dbus_method()
    def top_flows(self, n: "i") -> "s":
        return self.base.dbus_analyzer_top_flows(n)

    @dbus_signal()
    def alert(self, proto: "s", pps: "i") -> "si":
        return [proto, pps]


class TrafficAnalyzer(ProcessBase):
    def __init__(self) -> None:
        super().__init__(
            name="traffic_analyzer",
            version="0.2.0",
            description="Windowed traffic aggregation for the traffic pipeline",
        )
        self.window: Window | None = None
        self._sensors: dict[str, object] = {}
        self._last_alert = 0.0

    async def start_dbus(self) -> bool:
        self.bus = DBusManager(
            logger=self.logger,
            busname="traffic_analyzer",
            bus_prefix=self.bus_prefix,
        )
        self.iface = TrafficAnalyzerContract(f"{self.bus_prefix}.TrafficAnalyzer", self)
        self.bus.add_interface("analyzer", self.iface)
        await self.bus.start()
        self.logger.info("traffic_analyzer started: bus=%s", self.bus.busname)
        return True

    def update_tasks(self) -> None:
        if self.window is None:
            seconds = self.config["analyzer"].getfloat("window_s", fallback=10.0)
            self.window = Window(seconds)
        if "scanner" not in self.tasklist:
            self.tasklist["scanner"] = asyncio.create_task(self._scan_sensors(), name="scanner")
        if "ticker" not in self.tasklist:
            self.tasklist["ticker"] = asyncio.create_task(self._ticker(), name="ticker")

    def dbus_analyzer_summary(self) -> str:
        now = time.time()
        counts = self.window.counts(now)
        return json.dumps(
            {
                "sensors": len(self._sensors),
                "window_s": self.window.seconds,
                "pps": round(self.window.pps(now), 2),
                "packets": len(self.window),
                "bytes": self.window.total_bytes(now),
                "by_proto": dict(counts),
            }
        )

    def dbus_analyzer_top_flows(self, n: int) -> str:
        limit = max(1, min(int(n or 5), 50))
        rows = [{"flow": flow, "packets": count} for flow, count in self.window.top(limit)]
        return json.dumps(rows)

    def _on_packet(self, row_json: str) -> None:
        try:
            row = json.loads(row_json)
            ts = float(row.get("ts") or time.time())
            self.window.add(ts, row.get("proto", "?"), flow_key(row), row.get("length", 0))
        except (TypeError, ValueError, json.JSONDecodeError):
            self.logger.warning("discarding malformed packet row")

    async def _ticker(self) -> None:
        period = self.config["analyzer"].getfloat("eval_s", fallback=2.0)
        try:
            while not self.exitevent.is_set():
                await self.do_waitexit(timeout=period)
                self._maybe_alert()
        except asyncio.CancelledError:
            pass

    def _maybe_alert(self) -> None:
        threshold = self.config["analyzer"].getfloat("alert_pps", fallback=50.0)
        cooldown = self.config["analyzer"].getfloat("cooldown_s", fallback=10.0)
        now = time.time()
        pps = self.window.pps(now)
        if threshold <= 0 or pps < threshold or now - self._last_alert < cooldown:
            return
        counts = self.window.counts(now)
        proto = counts.most_common(1)[0][0] if counts else "?"
        self._last_alert = now
        self.iface.alert(proto, int(round(pps)))
        self.logger.warning("alert: proto=%s pps=%.1f", proto, pps)

    async def _scan_sensors(self) -> None:
        period = self.config["analyzer"].getfloat("scan_s", fallback=5.0)
        ifname = f"{self.bus_prefix}.{_SENSOR_IFACE}"
        objpath = f"{self.bus._obj_root}/{_SENSOR_PATH}"
        try:
            while not self.exitevent.is_set():
                await self.bus.update_friendbus()
                names = self.bus.query_friend_busname("traffic_sensor")
                for name in names:
                    if name in self._sensors:
                        continue
                    try:
                        proxy = await self.bus.get_friend_bus(
                            name, ifname=ifname, objpath=objpath
                        )
                        proxy.on_packet(self._on_packet)
                        self._sensors[name] = proxy
                        self.logger.info("subscribed to %s", name)
                    except Exception:
                        self.logger.exception("cannot subscribe to %s", name)
                for name in list(self._sensors):
                    if name not in names:
                        del self._sensors[name]
                        self.logger.info("unsubscribed from %s", name)
                await self.do_waitexit(timeout=period)
        except asyncio.CancelledError:
            pass


def main() -> None:
    TrafficAnalyzer().start()


if __name__ == "__main__":
    main()
