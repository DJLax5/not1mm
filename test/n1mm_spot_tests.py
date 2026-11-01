"""Tests for the N1MM spot broadcast."""

import socket
import xml.etree.ElementTree as ET

from not1mm.lib.n1mm import N1MM


def test_send_spot_xml():
    receiver = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    receiver.bind(("127.0.0.1", 0))
    receiver.settimeout(2)
    port = receiver.getsockname()[1]
    n1mm = N1MM(spotport=f"127.0.0.1:{port}")
    n1mm.set_station_name("TENT")
    n1mm.spot_info["dxcall"] = "K6GTE"
    n1mm.spot_info["frequency"] = "14025.5"
    n1mm.spot_info["spottercall"] = "DM7HB"
    n1mm.spot_info["comment"] = "CW 20 dB <up>"
    n1mm.spot_info["mode"] = "CW"
    n1mm.spot_info["timestamp"] = "2026-11-01 12:34:56"
    n1mm.send_spot()
    data, _ = receiver.recvfrom(4096)
    receiver.close()
    root = ET.fromstring(data)
    assert root.tag == "spot"
    assert [child.tag for child in root] == [
        "app",
        "StationName",
        "dxcall",
        "frequency",
        "spottercall",
        "comment",
        "action",
        "mode",
        "status",
        "statuslist",
        "timestamp",
    ]
    assert root.findtext("StationName") == "TENT"
    assert root.findtext("dxcall") == "K6GTE"
    assert root.findtext("frequency") == "14025.5"
    assert root.findtext("comment") == "CW 20 dB <up>"
    assert root.findtext("action") == "add"
    assert root.findtext("timestamp") == "2026-11-01 12:34:56"


def test_send_spot_bad_address_does_not_raise():
    n1mm = N1MM(spotport="300.1.1.1:12060 bad 127.0.0.1:x")
    n1mm.send_spot()
