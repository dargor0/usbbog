from traffic_common import Window, flow_key


def test_flow_key_uses_endpoints_and_proto():
    row = {
        "src": "10.0.0.1", "sport": 1234,
        "dst": "10.0.0.2", "dport": 443,
        "proto": "TCP",
    }
    assert flow_key(row) == "10.0.0.1:1234->10.0.0.2:443/TCP"


def test_window_prunes_old_events():
    window = Window(10)
    window.add(100.0, "TCP", "a", 60)
    window.add(105.0, "UDP", "b", 40)
    window.add(111.0, "TCP", "a", 100)
    window.prune(now=111.0)
    assert len(window) == 2
    assert window.counts(now=111.0) == {"TCP": 1, "UDP": 1}
    assert window.pps(now=111.0) == 0.2
    assert window.total_bytes(now=111.0) == 140


def test_window_top_flows_orders_by_packets():
    window = Window(60)
    for _ in range(3):
        window.add(200.0, "TCP", "a", 10)
    window.add(200.0, "UDP", "b", 10)
    assert window.top(1, now=200.0) == [("a", 3)]
