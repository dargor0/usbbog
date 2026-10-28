"""Controlador de ocho displays de 7 segmentos para Nexys4 DDR.

Recibe ocho digitos BCD (4 bits cada uno), multiplexa un display a la vez y
genera los 7 segmentos y los 8 anodos. Los anodos y segmentos son activos en
bajo por defecto (Nexys4 DDR); se pueden cambiar en elaboracion.

Uso:
    python3 eight_digit_display.py      # genera eight_digit_display.v
"""

from pathlib import Path

from myhdl import ResetSignal, Signal, always_comb, always_seq, block, instances, intbv

from sevensegdec import read_table, sevensegdec

SEG_TABLE = read_table(str(Path(__file__).with_name("sevenseg_table.txt")))


@block
def eight_digit_display(
    clk,
    rst,
    bcd0,
    bcd1,
    bcd2,
    bcd3,
    bcd4,
    bcd5,
    bcd6,
    bcd7,
    seg,
    an,
    clk_freq_hz=100_000_000,
    refresh_hz=1000,
    invert=True,
    anode_active_low=True,
):
    """Multiplexa ocho digitos BCD en un display de 7 segmentos.

    Args:
        clk: reloj del sistema (100 MHz en Nexys4 DDR).
        rst: ResetSignal activo en bajo.
        bcd0..bcd7: entradas BCD de 4 bits, una por digito.
        seg: salida de 7 segmentos (activa en bajo si invert=True).
        an: salida de 8 anodos (activa en bajo si anode_active_low=True).
        clk_freq_hz: frecuencia de clk, para calcular el divisor.
        refresh_hz: frecuencia de conmutacion por digito (no del frame).
        invert: invierte los segmentos (Nexys4 DDR: True).
        anode_active_low: anodos activos en bajo (Nexys4 DDR: True).
    """
    if refresh_hz <= 0:
        raise ValueError("refresh_hz must be > 0")
    scan_cycles = int(round(clk_freq_hz / refresh_hz))
    if scan_cycles < 1:
        raise ValueError("refresh_hz too high for clk_freq_hz")

    scan_width = max(1, (scan_cycles - 1).bit_length())
    scan_cnt = Signal(intbv(0)[scan_width:])
    digit = Signal(intbv(0)[3:])
    bcd_mux = Signal(intbv(0)[4:])

    @always_seq(clk.posedge, reset=rst)
    def scan():
        if scan_cnt == scan_cycles - 1:
            scan_cnt.next = 0
            digit.next = 0 if digit == 7 else digit + 1
        else:
            scan_cnt.next = scan_cnt + 1

    @always_comb
    def mux_bcd():
        if digit == 0:
            bcd_mux.next = bcd0
        elif digit == 1:
            bcd_mux.next = bcd1
        elif digit == 2:
            bcd_mux.next = bcd2
        elif digit == 3:
            bcd_mux.next = bcd3
        elif digit == 4:
            bcd_mux.next = bcd4
        elif digit == 5:
            bcd_mux.next = bcd5
        elif digit == 6:
            bcd_mux.next = bcd6
        else:
            bcd_mux.next = bcd7

    @always_comb
    def anodes():
        if not rst:
            an.next = 0xFF  # todos apagados durante reset
        elif anode_active_low:
            an.next = 0xFF ^ (1 << digit)
        else:
            an.next = 1 << digit

    decoder = sevensegdec(bcd_mux, seg, SEG_TABLE, invert)
    return instances()


def convert_verilog():
    """Convierte el bloque a eight_digit_display.v con valores de Nexys4 DDR."""
    clk = Signal(False)
    rst = ResetSignal(0, active=0, isasync=True)
    bcd = [Signal(intbv(0)[4:]) for _ in range(8)]
    seg = Signal(intbv(0)[7:])
    an = Signal(intbv(0)[8:])

    inst = eight_digit_display(
        clk,
        rst,
        *bcd,
        seg,
        an,
        clk_freq_hz=100_000_000,
        refresh_hz=1000,
        invert=True,
        anode_active_low=True,
    )
    inst.convert(hdl="Verilog", testbench=False)
    print("Generado: eight_digit_display.v")


if __name__ == "__main__":
    convert_verilog()
