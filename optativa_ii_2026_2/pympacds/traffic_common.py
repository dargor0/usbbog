"""Utilidades compartidas por los servicios del pipeline de tráfico.

Solo contiene lógica pura (sin D-Bus ni scapy) para poder probarla sin
levantar los servicios.
"""

from __future__ import annotations

import time
from collections import Counter, deque


def flow_key(row: dict) -> str:
    """Clave estable de flujo a partir de una fila de paquete."""
    return "{src}:{sport}->{dst}:{dport}/{proto}".format(
        src=row.get("src", "?"),
        sport=row.get("sport", 0),
        dst=row.get("dst", "?"),
        dport=row.get("dport", 0),
        proto=row.get("proto", "?"),
    )


class Window:
    """Ventana deslizante de eventos (ts, proto, flujo, longitud)."""

    def __init__(self, seconds: float) -> None:
        if seconds <= 0:
            raise ValueError("window seconds must be > 0")
        self.seconds = float(seconds)
        self._events: deque[tuple[float, str, str, int]] = deque()

    def add(self, ts: float, proto: str, flow: str, length: int = 0) -> None:
        self._events.append((float(ts), str(proto), str(flow), int(length)))

    def prune(self, now: float | None = None) -> None:
        cutoff = (time.time() if now is None else now) - self.seconds
        while self._events and self._events[0][0] < cutoff:
            self._events.popleft()

    def __len__(self) -> int:
        return len(self._events)

    def pps(self, now: float | None = None) -> float:
        self.prune(now)
        return len(self._events) / self.seconds

    def counts(self, now: float | None = None) -> Counter:
        self.prune(now)
        return Counter(event[1] for event in self._events)

    def top(self, n: int = 5, now: float | None = None) -> list[tuple[str, int]]:
        self.prune(now)
        return Counter(event[2] for event in self._events).most_common(n)

    def total_bytes(self, now: float | None = None) -> int:
        self.prune(now)
        return sum(event[3] for event in self._events)
