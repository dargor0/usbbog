"""Pruebas MyHDL del contador 0-9 con display de 7 segmentos.

Ejecutar desde este directorio:
    python3 -m pytest -q
"""

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

from counter_7seg import SEG_TABLE, counter_7seg

CLK_HZ = 100_000_000
CYCLES = 3
PERIOD_S = CYCLES / CLK_HZ


@block
def tb():
    clk = Signal(False)
    rst = ResetSignal(0, active=0, isasync=True)
    pause = Signal(False)
    up = Signal(True)
    count = Signal(intbv(0)[4:])
    seg = Signal(intbv(0)[7:])

    dut = counter_7seg(clk, rst, pause, up, count, seg, period_s=PERIOD_S, clk_freq_hz=CLK_HZ)

    @always(delay(5))
    def clkgen():
        clk.next = not clk

    @instance
    def stimulus():
        def tick(n):
            for _ in range(n):
                yield clk.posedge
                yield delay(1)

        def check(expected, context):
            assert int(count) == expected, (
                f"{context}: count={int(count)}, esperado={expected}"
            )
            assert int(seg) == SEG_TABLE[expected], (
                f"{context}: seg={int(seg):07b}, "
                f"esperado={SEG_TABLE[expected]:07b}"
            )

        # Reset asincrono activo en bajo.
        rst.next = 0
        yield delay(12)
        rst.next = 1
        yield clk.posedge
        yield delay(1)
        check(0, "reset")

        # Ascendente: 1, 2, 3, 4.
        for expected in (1, 2, 3, 4):
            for event in tick(CYCLES):
                yield event
            check(expected, f"subiendo a {expected}")

        # Pausa: la cuenta y el display se congelan.
        pause.next = 1
        for event in tick(2 * CYCLES):
            yield event
        check(4, "pausa")

        # Al reanudar, el prescaler continua donde estaba.
        pause.next = 0
        for event in tick(CYCLES):
            yield event
        check(5, "reanudando")

        # Termina el ascenso y comprueba el wrap 9 -> 0.
        for expected in (6, 7, 8, 9, 0):
            for event in tick(CYCLES):
                yield event
            check(expected, f"subiendo a {expected}")

        # Reset para probar el descenso desde 0.
        rst.next = 0
        yield delay(12)
        rst.next = 1
        yield clk.posedge
        yield delay(1)
        check(0, "reset antes de bajar")

        up.next = 0
        for expected in (9, 8, 7, 6, 5, 4, 3, 2, 1, 0):
            for event in tick(CYCLES):
                yield event
            check(expected, f"bajando a {expected}")

        raise StopSimulation

    return dut, clkgen, stimulus


def test_seg_table_file():
    assert len(SEG_TABLE) == 16
    assert SEG_TABLE[0] == 0b1111110
    assert SEG_TABLE[9] == 0b1111011


def test_counter_7seg():
    sim = tb()
    sim.config_sim(trace=False)
    sim.run_sim()
