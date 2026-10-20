# pympacds traffic pipeline

Pipeline de **tres servicios pympacds** que cooperan por D-Bus y descubrimiento:

```
traffic_sensor ──packet(row)──▶ traffic_analyzer ──alert(proto,pps)──▶ traffic_guard
      │                                │                                   │
  SQLite (packets)              ventana deslizante                  alerts.jsonl
  (CAP_NET_RAW)                 (sin privilegios)                   (sin privilegios)
```

- **`traffic_sensor`**: captura con [scapy](https://scapy.net/), persiste en
  SQLite y publica cada fila por la señal `packet`.
- **`traffic_analyzer`**: descubre sensores, se suscribe a `packet`, agrega en
  una ventana deslizante y emite `alert` al superar un umbral de paquetes/s.
- **`traffic_guard`**: descubre analizadores, se suscribe a `alert` y aplica la
  política (por defecto registra la alerta con enfriamiento).

Ningún servicio importa a otro: solo comparten el `bus_prefix` y los contratos
D-Bus. El sistema **no funciona con uno solo**: el analizador necesita al menos
un sensor y el guardián necesita al analizador.

## Contratos y descubrimiento

| Servicio | busname | contrato | provides | requires | señal |
|---|---|---|---|---|---|
| sensor | `traffic_sensor` | `TrafficSensor` | `traffic.capture` | — | `packet(row)` |
| analyzer | `traffic_analyzer` | `TrafficAnalyzer` | `traffic.analysis` | `traffic.capture` | `alert(proto,pps)` |
| guard | `traffic_guard` | `TrafficGuard` | `traffic.policy` | `traffic.analysis` | — |

El analizador descubre con `query_friend_busname("traffic_sensor")` y se
suscribe con `proxy.on_packet(...)`. El guardián hace lo mismo con
`"traffic_analyzer"` y `proxy.on_alert(...)`. Los tags `provides`/`requires`
se publican en el contrato `Health` de cada servicio.

## Contenido

```
.
├── traffic_sensor.py       # captura + SQLite + señal packet
├── traffic_analyzer.py     # descubrimiento + ventana + señal alert
├── traffic_guard.py        # descubrimiento + política
├── traffic_common.py       # flow_key y Window (lógica pura)
├── traffic_sensor.ini
├── traffic_analyzer.ini
├── traffic_guard.ini
├── requirements.txt
├── pyproject.toml          # consolas traffic-sensor/analyzer/guard
├── tests/
│   └── test_window.py
├── LICENSE
└── README.md
```

## Requisitos

- Linux con **D-Bus (system bus)** y **systemd**.
- **Python >= 3.10**.
- `pympacds`; `scapy` solo para el sensor.
- El sensor necesita capturar paquetes (`CAP_NET_RAW`): `root` o la capacidad
  sobre el ejecutable.

Dispositivos probados/objetivo:

- Raspberry Pi con Raspberry Pi OS (arm64/armhf).
- NVIDIA Jetson Nano (necesita Python >= 3.10; L4T 18.04 trae 3.6).
- Máquina virtual Ubuntu 22.04/24.04.

## Instalación

El paquete `python3-pympacds` es `all`: **no depende de la arquitectura**
(amd64/arm64/armhf).

### Con PPA (solo Ubuntu)

```bash
sudo add-apt-repository ppa:dargor0/mpacds
sudo apt update
sudo apt install python3-pympacds
```

El paquete deja la política D-Bus y el usuario del sistema configurados; **no**
hace falta ejecutar `pympacds-admin setup`. `add-apt-repository` con un PPA es
de Ubuntu: en Debian/Raspberry Pi OS usa la instalación manual o pip.

### PPA manual (Debian/RPi OS o sin add-apt-repository)

```bash
sudo install -d -m 0755 /etc/apt/keyrings
curl -fsSL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=\
0x2A77ABE07D50273F799B17FE40150F7CD2A2037E" \
  | sudo gpg --dearmor --yes -o /etc/apt/keyrings/dargor0-mpacds.gpg

sudo tee /etc/apt/sources.list.d/dargor0-mpacds.sources >/dev/null <<'EOF'
Types: deb
URIs: https://ppa.launchpadcontent.net/dargor0/mpacds/ubuntu/
Suites: noble
Components: main
Signed-By: /etc/apt/keyrings/dargor0-mpacds.gpg
EOF

sudo apt update
sudo apt install python3-pympacds
```

Cambia `noble` por la suite publicada para tu versión (`jammy`, `oracular`,
`resolute`...). Consulta
<https://launchpad.net/~dargor0/+archive/ubuntu/mpacds>. En Debian/RPi OS el
PPA no es nativo: si las dependencias no cuadran, usa pip.

### Directa en el sistema (pip, sin venv)

```bash
sudo apt install python3-pip          # Debian/RPi OS
sudo python3 -m pip install --break-system-packages pympacds scapy
sudo pympacds-admin setup
pympacds-admin --version
```

El servicio lo lanza **systemd** con el Python del sistema, que no activa
entornos virtuales: **no uses `venv`** para los servicios. `--break-system-packages`
es necesario en Debian 12+/Ubuntu 24.04 (PEP 668). `setup` crea
`pympacds-user`, `/var/log/pympacds` y la política D-Bus. Para despliegues
mínimos: `sudo SKIP_CYTHON=1 python3 -m pip install --break-system-packages
--no-binary dbus-fast pympacds`.

## Configuración

Los tres INI comparten `[dbus]`; cambia solo la sección propia:

```ini
# traffic_sensor.ini
[dbus]
bus_prefix = org.pympacds.test
discovery_enabled = true

[sensor]
iface = eth0
bpf = tcp or udp
db_path = traffic.db
flush_s = 2
autostart = true
```

```ini
# traffic_analyzer.ini
[analyzer]
window_s = 10
alert_pps = 50
cooldown_s = 10
scan_s = 5
eval_s = 2
```

```ini
# traffic_guard.ini
[guard]
threshold_pps = 50
cooldown_s = 5
alerts_path = alerts.jsonl
scan_s = 5
```

El `bus_prefix` **debe ser el mismo** en los tres. Los valores también se
pueden sobrescribir con `PYMPACDS_DBUS_BUS_TYPE=session`, etc.

## Ejecución

Tres terminales (el orden no importa: el descubrimiento reintenta cada
`scan_s`):

```bash
# terminal 1 — captura (requiere privilegios de red)
sudo python3 traffic_sensor.py -c traffic_sensor.ini

# terminal 2 — análisis (sin privilegios)
python3 traffic_analyzer.py -c traffic_analyzer.ini

# terminal 3 — política (sin privilegios)
python3 traffic_guard.py -c traffic_guard.ini
```

Con el paquete instalado (`pip install -e .`), usa `traffic-sensor`,
`traffic-analyzer` y `traffic-guard` con su `-c`.

Verificación:

```bash
pympacds-admin list
busctl --system call org.pympacds.test.traffic_analyzer \
  /org/pympacds/test/analyzer org.pympacds.test.TrafficAnalyzer Summary
busctl --system call org.pympacds.test.traffic_guard \
  /org/pympacds/test/guard org.pympacds.test.TrafficGuard Status
```

## API D-Bus

Sensor (`/org/pympacds/test/traffic`):

```bash
busctl --system call org.pympacds.test.traffic_sensor \
  /org/pympacds/test/traffic org.pympacds.test.TrafficSensor Stats
busctl --system call org.pympacds.test.traffic_sensor \
  /org/pympacds/test/traffic org.pympacds.test.TrafficSensor \
  Start ss eth0 "tcp or udp"
busctl --system call org.pympacds.test.traffic_sensor \
  /org/pympacds/test/traffic org.pympacds.test.TrafficSensor Stop
```

Analizador (`/org/pympacds/test/analyzer`): `Summary` y `TopFlows i 5`.

Guardián (`/org/pympacds/test/guard`): `Status` y `SetThreshold i 100`.

Señales: `packet(row)` (sensor → analyzer) y `alert(proto, pps)`
(analyzer → guard). `Health` está activo por defecto en los tres.

## Generar tráfico de prueba

El sensor solo verá tráfico que pase por la interfaz configurada. En una VM o
Raspberry Pi:

```bash
ping -c 20 8.8.8.8
curl -s https://example.com >/dev/null
# o, si está instalado:
iperf3 -c <servidor> -t 10
```

Para `lo`, usa `iface = lo` y genera tráfico local (`curl localhost`).

## Almacenamiento y alertas

SQLite:

```bash
sqlite3 traffic.db \
  "SELECT proto, count(*) FROM packets GROUP BY proto;"
```

Alertas (JSON Lines):

```bash
cat alerts.jsonl
```

## Como servicio systemd

Instala el paquete y sus consolas:

```bash
sudo python3 -m pip install --break-system-packages .
```

Registra cada servicio (solo el sensor necesita `--user root`):

```bash
sudo mkdir -p /etc/pympacds
sudo cp traffic_sensor.ini traffic_analyzer.ini traffic_guard.ini /etc/pympacds/

sudo pympacds-admin install traffic_sensor \
  --program /usr/local/bin/traffic-sensor \
  --config /etc/pympacds/traffic_sensor.ini --user root --start
sudo pympacds-admin install traffic_analyzer \
  --program /usr/local/bin/traffic-analyzer \
  --config /etc/pympacds/traffic_analyzer.ini --start
sudo pympacds-admin install traffic_guard \
  --program /usr/local/bin/traffic-guard \
  --config /etc/pympacds/traffic_guard.ini --start
```

Estado y logs:

```bash
systemctl status pympacds-traffic_sensor pympacds-traffic_analyzer pympacds-traffic_guard
journalctl -u pympacds-traffic_sensor -f
```

Notas de seguridad de `pympacds-admin`:

- Las rutas deben pertenecer a `root`/`pympacds-user` y no ser escribibles por
  otros (no `/tmp`).
- Para capturar tráfico: `--user root` (pide confirmación interactiva) o un
  drop-in con `AmbientCapabilities=CAP_NET_RAW`.
- Usa `--dry-run` para previsualizar.

## Pruebas

```bash
python3 -m pytest -q
```

## Estado

- Los tres servicios están implementados, con sus INI, utilidades y pruebas.
- Verificado: sintaxis (`py_compile`) y lógica de `flow_key`/`Window` (pytest).
- No verificado en este repositorio: integración D-Bus real; requiere
  `pympacds`, `scapy`, un bus y permisos de captura.

## Licencia

MIT. Ver [LICENSE](LICENSE).
