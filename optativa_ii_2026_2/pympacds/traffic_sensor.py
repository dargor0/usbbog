"""traffic_sensor — captura paquetes, los persiste y publica cada fila.

Run:  sudo python3 traffic_sensor.py -c traffic_sensor.ini

Es el único servicio del pipeline que necesita CAP_NET_RAW.
"""

from __future__ import annotations

import asyncio
import json
import os
import queue
import sqlite3
import time

from scapy.all import IP, TCP, UDP, AsyncSniffer

from pympacds.contracts import ServiceContract, dbus_method, dbus_signal
from pympacds.dbus import DBusManager
from pympacds.process import ProcessBase

_SCHEMA = """CREATE TABLE IF NOT EXISTS packets(
    ts REAL, src TEXT, dst TEXT, proto TEXT,
    sport INTEGER, dport INTEGER, length INTEGER, summary TEXT)"""


def packet_to_row(pkt) -> dict | None:
    """Convierte un paquete IP en una fila serializable (o None)."""
    if not pkt.haslayer(IP):
        return None
    l4 = pkt[TCP] if pkt.haslayer(TCP) else pkt[UDP] if pkt.haslayer(UDP) else None
    proto = "TCP" if pkt.haslayer(TCP) else "UDP" if pkt.haslayer(UDP) else "OTHER"
    return {
        "ts": time.time(),
        "src": pkt[IP].src,
        "dst": pkt[IP].dst,
        "proto": proto,
        "sport": int(l4.sport) if l4 is not None else 0,
        "dport": int(l4.dport) if l4 is not None else 0,
        "length": len(pkt),
        "summary": pkt.summary(),
    }


class TrafficSensorContract(ServiceContract):
    iface_name = "TrafficSensor"
    iface_version = "1.0.0"
    iface_provides = ["traffic.capture"]
    iface_requires = []

    def __init__(self, ifname: str, base: ProcessBase) -> None:
        super().__init__(ifname, base)
        self._require("dbus_sensor_start", "dbus_sensor_stop", "dbus_sensor_stats")

    @dbus_method()
    def start(self, iface: "s", bpf: "s") -> "b":
        return self.base.dbus_sensor_start(iface, bpf)

    @dbus_method()
    def stop(self) -> "b":
        return self.base.dbus_sensor_stop()

    @dbus_method()
    def stats(self) -> "s":
        return self.base.dbus_sensor_stats()

    @dbus_signal()
    def packet(self, row: "s") -> "s":
        return [row]


class TrafficSensor(ProcessBase):
    def __init__(self) -> None:
        super().__init__(
            name="traffic_sensor",
            version="0.2.0",
            description="Packet capture and persistence for the traffic pipeline",
        )
        self.sniffer: AsyncSniffer | None = None
        self.running = False
        self.q: queue.Queue = queue.Queue()
        self.rows = 0
        self.bytes = 0
        self.drops = 0
        self._autostarted = False

    async def start_dbus(self) -> bool:
        self.bus = DBusManager(
            logger=self.logger,
            busname="traffic_sensor",
            bus_prefix=self.bus_prefix,
        )
        self.iface = TrafficSensorContract(f"{self.bus_prefix}.TrafficSensor", self)
        self.bus.add_interface("traffic", self.iface)
        await self.bus.start()
        self.logger.info("traffic_sensor started: bus=%s", self.bus.busname)
        return True

    def update_tasks(self) -> None:
        if "writer" not in self.tasklist:
            self.tasklist["writer"] = asyncio.create_task(self._writer(), name="writer")
        if not self._autostarted and self.config["sensor"].getboolean(
            "autostart", fallback=True
        ):
            self._autostarted = True
            self.dbus_sensor_start(
                self.config["sensor"].get("iface", fallback=""),
                self.config["sensor"].get("bpf", fallback=""),
            )

    def dbus_sensor_start(self, iface: str, bpf: str) -> bool:
        if self.running:
            return True
        self.sniffer = AsyncSniffer(
            iface=iface or None,
            filter=bpf or None,
            prn=self._on_pkt,
            store=False,
        )
        self.sniffer.start()
        self.running = True
        self.logger.info("capture started: iface=%s bpf=%s", iface or "all", bpf or "none")
        return True

    def dbus_sensor_stop(self) -> bool:
        if self.sniffer is not None and self.running:
            self.sniffer.stop()
            self.logger.info("capture stopped")
        self.running = False
        return True

    def dbus_sensor_stats(self) -> str:
        return json.dumps(
            {
                "running": self.running,
                "packets": self.rows,
                "bytes": self.bytes,
                "drops": self.drops,
                "queue": self.q.qsize(),
            }
        )

    def _on_pkt(self, pkt) -> None:
        row = packet_to_row(pkt)
        if row is None:
            return
        if self.q.qsize() > 10000:
            self.drops += 1
            return
        self.q.put(row)

    async def _writer(self) -> None:
        path = self.config["sensor"].get("db_path", fallback="traffic.db")
        directory = os.path.dirname(os.path.abspath(path))
        os.makedirs(directory, exist_ok=True)
        conn = sqlite3.connect(path)
        conn.execute(_SCHEMA)
        flush_s = self.config["sensor"].getfloat("flush_s", fallback=2.0)
        try:
            while not self.exitevent.is_set():
                batch = []
                while len(batch) < 200:
                    try:
                        batch.append(self.q.get_nowait())
                    except queue.Empty:
                        break
                if batch:
                    conn.executemany(
                        "INSERT INTO packets VALUES (?,?,?,?,?,?,?,?)",
                        [
                            (
                                r["ts"], r["src"], r["dst"], r["proto"],
                                r["sport"], r["dport"], r["length"], r["summary"],
                            )
                            for r in batch
                        ],
                    )
                    conn.commit()
                    self.rows += len(batch)
                    self.bytes += sum(r["length"] for r in batch)
                    for r in batch:
                        self.iface.packet(json.dumps(r))
                await self.do_waitexit(timeout=flush_s)
        except asyncio.CancelledError:
            pass
        finally:
            conn.close()


def main() -> None:
    TrafficSensor().start()


if __name__ == "__main__":
    main()
