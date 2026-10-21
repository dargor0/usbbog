"""Contador 0-9 ascendente/descendente con pausa y periodo configurable.

El periodo se fija en elaboracion con ``period_s`` en segundos (admite
float; por defecto 1 s) y se convierte a ciclos con ``clk_freq_hz``. La salida
de cuenta se decodifica a 7 segmentos con ``sevensegdec``.
"""

from pathlib import Path

from myhdl import ResetSignal, Signal, always_seq, block, instances, intbv

from sevensegdec import read_table, sevensegdec

TABLE_PATH = Path(__file__).with_name("sevenseg_table.txt")

if not TABLE_PATH.is_file():
    raise FileNotFoundError(TABLE_PATH)
SEG_TABLE = read_table(str(TABLE_PATH))
if len(SEG_TABLE) != 16 or not any(SEG_TABLE):
    raise ValueError(f"tabla invalida: {TABLE_PATH}")


@block
def counter_7seg(clk, rst, pause, up, count, seg,
                 period_s=1.0, clk_freq_hz=100_000_000, invert=False):
    """Contador BCD 0-9 con pausa, sentido y periodo en segundos.

    Args:
        clk: reloj.
        rst: ResetSignal (activo en el nivel que se haya declarado).
        pause: si esta activo, congela cuenta y prescaler.
        up: 1 cuenta ascendente; 0 descendente.
        count: salida de 4 bits (0-9).
        seg: salida de 7 bits para el display.
        period_s: segundos entre cambios (admite float); por defecto 1 s.
        clk_freq_hz: frecuencia del reloj; Nexys4 DDR usa 100 MHz.
        invert: invierte los segmentos si el display es activo en bajo.
    """
    cycles = int(round(period_s * clk_freq_hz))
    if cycles < 1:
        raise ValueError("period_s demasiado pequeno para clk_freq_hz")

    # Ancho minimo para representar cycles - 1.
    pw = max(1, (cycles - 1).bit_length())
    presc = Signal(intbv(0)[pw:])

    @always_seq(clk.posedge, reset=rst)
    def logic():
        if not pause:
            if presc == cycles - 1:
                presc.next = 0
                if up:
                    count.next = 0 if count == 9 else count + 1
                else:
                    count.next = 9 if count == 0 else count - 1
            else:
                presc.next = presc + 1

    decoder = sevensegdec(count, seg, SEG_TABLE, invert)
    return instances()


@block
def counter_7seg_nexys(clk, rst, pause, up, invert, count, seg, anodes,
                       period_s=1.0, clk_freq_hz=100_000_000):
    """Top-level para Nexys4 DDR (100 MHz): cuenta, LEDs y un digito."""
    core = counter_7seg(
        clk, rst, pause, up, count, seg,
        period_s=period_s, clk_freq_hz=clk_freq_hz, invert=invert
    )

    @always_seq(clk.posedge, reset=rst)
    def anodes_logic():
        # Solo el digito 0; anodos activos en bajo.
        anodes.next = 0b11111110

    return instances()


def convert_verilog(period_s=1.0):
    """Convierte solo counter_7seg_nexys a Verilog (Nexys4 DDR, 100 MHz)."""
    clk = Signal(False)
    rst = ResetSignal(0, active=0, isasync=True)
    pause = Signal(False)
    up = Signal(True)
    invert = Signal(False)
    count = Signal(intbv(0)[4:])
    seg = Signal(intbv(0)[7:])
    anodes = Signal(intbv(0)[8:])

    inst = counter_7seg_nexys(
        clk, rst, pause, up, invert, count, seg, anodes,
        period_s=period_s, clk_freq_hz=100_000_000
    )
    inst.convert(hdl="Verilog", testbench=False)
    print("Generado: counter_7seg_nexys.v")


if __name__ == "__main__":
    convert_verilog()
