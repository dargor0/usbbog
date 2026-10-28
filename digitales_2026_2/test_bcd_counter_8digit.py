"""Pruebas basicas del contador BCD de 8 digitos."""

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

from bcd_counter_8digit import bcd_counter_8digit

SLOW_CYCLES = 10
FAST_CYCLES = 5


@block
def tb():
    clk = Signal(False)
    rst = ResetSignal(0, active=0, isasync=True)
    pause = Signal(False)
    up = Signal(True)
    fast = Signal(False)
    rst_count = Signal(False)
    bcd = [Signal(intbv(0)[4:]) for _ in range(8)]
    seg = Signal(intbv(0)[7:])
    an = Signal(intbv(0)[8:])

    dut = bcd_counter_8digit(
        clk,
        rst,
        pause,
        up,
        fast,
        rst_count,
        *bcd,
        seg,
        an,
        clk_freq_hz=100,
        count_hz=10,
        fast_hz=20,
        refresh_hz=100,
        invert=True,
        anode_active_low=True,
    )

    @always(delay(5))
    def clkgen():
        clk.next = not clk

    @instance
    def stimulus():
        def wait_cycles(n):
            for _ in range(n):
                yield clk.posedge
                yield delay(1)

        def values():
            return [int(x) for x in bcd]

        # Reset del sistema (activo en bajo).
        rst.next = 0
        yield delay(12)
        rst.next = 1
        yield clk.posedge
        yield delay(1)
        assert values() == [0] * 8, f"reset: {values()}"

        # Pausa: debe congelar la cuenta.
        pause.next = 1
        for event in wait_cycles(3 * SLOW_CYCLES):
            yield event
        assert values() == [0] * 8, f"pausa: {values()}"

        # 1 cuenta/s -> con clk de prueba, 10 ciclos por cuenta.
        pause.next = 0
        up.next = 1
        fast.next = 0
        for event in wait_cycles(SLOW_CYCLES):
            yield event
        assert values()[0] == 1, f"lenta: {values()}"

        # Pausa en medio de la cuenta.
        pause.next = 1
        for event in wait_cycles(2 * SLOW_CYCLES):
            yield event
        assert values()[0] == 1, f"pausa media: {values()}"
        pause.next = 0

        # 20 cuentas/s -> 5 ciclos por cuenta.
        fast.next = 1
        for event in wait_cycles(FAST_CYCLES):
            yield event
        assert values()[0] == 2, f"rapida: {values()}"

        # Acarreo BCD: 2 -> ... -> 9 -> 0 y digito 1 = 1.
        for event in wait_cycles(8 * FAST_CYCLES):
            yield event
        assert values()[0] == 0 and values()[1] == 1, f"acarreo: {values()}"

        # Reset del contador, activo en alto, independiente del reset del sistema.
        rst_count.next = 1
        for event in wait_cycles(2):
            yield event
        rst_count.next = 0
        assert values() == [0] * 8, f"rst_count: {values()}"

        # Descendente desde 00000000 -> 99999999 (prestamo en cadena).
        up.next = 0
        fast.next = 1
        for event in wait_cycles(FAST_CYCLES + 1):
            yield event
        assert values() == [9] * 8, f"descendente: {values()}"

        raise StopSimulation

    return dut, clkgen, stimulus


def test_bcd_counter_8digit():
    sim = tb()
    sim.config_sim(trace=False)
    sim.run_sim()
