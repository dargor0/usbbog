"""Pruebas basicas del controlador de ocho displays de 7 segmentos."""

from myhdl import (
    ResetSignal,
    Signal,
    StopSimulation,
    always,
    block,
    delay,
    instance,
    intbv,
)

from eight_digit_display import SEG_TABLE, eight_digit_display

DIGITS = 8


@block
def tb():
    clk = Signal(False)
    rst = ResetSignal(0, active=0, isasync=True)
    bcd_values = [0, 1, 2, 3, 4, 5, 8, 9]
    bcd = [Signal(intbv(v)[4:]) for v in bcd_values]
    seg = Signal(intbv(0)[7:])
    an = Signal(intbv(0)[8:])

    dut = eight_digit_display(
        clk,
        rst,
        *bcd,
        seg,
        an,
        clk_freq_hz=DIGITS,
        refresh_hz=DIGITS,
        invert=True,
        anode_active_low=True,
    )

    @always(delay(5))
    def clkgen():
        clk.next = not clk

    @instance
    def stimulus():
        # Reset asincrono activo en bajo: todos los anodos apagados.
        rst.next = 0
        yield delay(12)
        yield delay(1)
        assert int(an) == 0xFF, f"reset: an={int(an):08b}"

        rst.next = 1
        yield clk.posedge
        yield delay(1)

        seen = []
        for _ in range(DIGITS):
            value = int(an)
            active = [i for i in range(DIGITS) if ((value >> i) & 1) == 0]
            assert len(active) == 1, f"anodos no one-hot: {value:08b}"
            digit = active[0]
            expected = (~SEG_TABLE[int(bcd[digit])]) & 0x7F
            assert int(seg) == expected, (
                f"digito {digit}: seg={int(seg):07b}, esperado={expected:07b}"
            )
            seen.append(digit)
            yield clk.posedge
            yield delay(1)

        assert sorted(seen) == list(range(DIGITS)), f"secuencia: {seen}"
        raise StopSimulation

    return dut, clkgen, stimulus


def test_eight_digit_display():
    sim = tb()
    sim.config_sim(trace=False)
    sim.run_sim()
