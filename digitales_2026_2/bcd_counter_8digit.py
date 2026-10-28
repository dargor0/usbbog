"""Contador BCD de 8 digitos (00000000 a 99999999) para Nexys4 DDR.

Cada digito es un contador BCD independiente; se encadenan por acarreo para
formar un contador de 8 digitos. La salida se muestra en los ocho displays de
7 segmentos mediante ``eight_digit_display``.

Entradas de control:
    pause      : 1 congela la cuenta y el divisor de frecuencia.
    up         : 1 cuenta ascendente; 0 descendente.
    fast       : 0 = 1 cuenta/s; 1 = 20 cuentas/s.
    rst_count  : reset del contador, activo en alto, independiente de ``rst``.
"""

from myhdl import ResetSignal, Signal, always_comb, always_seq, block, instances, intbv

from eight_digit_display import eight_digit_display


@block
def bcd_digit(clk, rst, rst_count, en, up, bcd, carry):
    """Un digito BCD 0-9 con acarreo/prestamo combinacional."""

    @always_comb
    def carry_logic():
        if en:
            if up:
                carry.next = (bcd == 9)
            else:
                carry.next = (bcd == 0)
        else:
            carry.next = False

    @always_seq(clk.posedge, reset=rst)
    def count():
        if rst_count:
            bcd.next = 0
        elif en:
            if up:
                bcd.next = 0 if bcd == 9 else bcd + 1
            else:
                bcd.next = 9 if bcd == 0 else bcd - 1

    return instances()


@block
def bcd_digit_last(clk, rst, rst_count, en, up, bcd):
    """Ultimo digito: no necesita acarreo de salida."""

    @always_seq(clk.posedge, reset=rst)
    def count():
        if rst_count:
            bcd.next = 0
        elif en:
            if up:
                bcd.next = 0 if bcd == 9 else bcd + 1
            else:
                bcd.next = 9 if bcd == 0 else bcd - 1

    return count


@block
def bcd_counter_8digit(
    clk,
    rst,
    pause,
    up,
    fast,
    rst_count,
    seg,
    an,
    clk_freq_hz=100_000_000,
    count_hz=1,
    fast_hz=20,
    refresh_hz=1000,
    invert=True,
    anode_active_low=True,
):
    """Contador BCD de 8 digitos con pausa, sentido y velocidad.

    Parámetros de elaboración:
        clk_freq_hz : frecuencia de ``clk`` (100 MHz en Nexys4 DDR).
        count_hz    : cuentas por segundo con ``fast = 0`` (1 por defecto).
        fast_hz     : cuentas por segundo con ``fast = 1`` (20 por defecto).
        refresh_hz  : refresco por digito del display (1000 por defecto).
        invert, anode_active_low : polaridad de la Nexys4 DDR.
    """
    if count_hz <= 0 or fast_hz <= 0:
        raise ValueError("count_hz and fast_hz must be > 0")
    slow_cycles = int(round(clk_freq_hz / count_hz))
    fast_cycles = int(round(clk_freq_hz / fast_hz))
    if slow_cycles < 1 or fast_cycles < 1:
        raise ValueError("count frequencies too high for clk_freq_hz")

    max_cycles = max(slow_cycles, fast_cycles)
    div_width = max(1, (max_cycles - 1).bit_length())
    div_cnt = Signal(intbv(0)[div_width:])
    tick = Signal(False)

    digits = [Signal(intbv(0)[4:]) for _ in range(8)]
    carries = [Signal(False) for _ in range(7)]

    @always_seq(clk.posedge, reset=rst)
    def timebase():
        tick.next = False
        if rst_count:
            div_cnt.next = 0
        elif not pause:
            if fast:
                if div_cnt >= fast_cycles - 1:
                    div_cnt.next = 0
                    tick.next = True
                else:
                    div_cnt.next = div_cnt + 1
            else:
                if div_cnt >= slow_cycles - 1:
                    div_cnt.next = 0
                    tick.next = True
                else:
                    div_cnt.next = div_cnt + 1

    digit_instances = []
    for i in range(7):
        en = tick if i == 0 else carries[i - 1]
        digit_instances.append(
            bcd_digit(clk, rst, rst_count, en, up, digits[i], carries[i])
        )
    digit_instances.append(
        bcd_digit_last(clk, rst, rst_count, carries[6], up, digits[7])
    )

    display = eight_digit_display(
        clk,
        rst,
        *digits,
        seg,
        an,
        clk_freq_hz=clk_freq_hz,
        refresh_hz=refresh_hz,
        invert=invert,
        anode_active_low=anode_active_low,
    )

    return instances()


def convert_verilog():
    """Convierte el contador completo a Verilog (Nexys4 DDR, 100 MHz)."""
    clk = Signal(False)
    rst = ResetSignal(0, active=0, isasync=True)
    pause = Signal(False)
    up = Signal(True)
    fast = Signal(False)
    rst_count = Signal(False)
    seg = Signal(intbv(0)[7:])
    an = Signal(intbv(0)[8:])

    inst = bcd_counter_8digit(
        clk,
        rst,
        pause,
        up,
        fast,
        rst_count,
        seg,
        an,
        clk_freq_hz=100_000_000,
        count_hz=1,
        fast_hz=20,
        refresh_hz=1000,
        invert=True,
        anode_active_low=True,
    )
    inst.convert(hdl="Verilog", testbench=False)
    print("Generado: bcd_counter_8digit.v")


if __name__ == "__main__":
    convert_verilog()
