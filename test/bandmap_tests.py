from not1mm.bandmap import Database


def _spot(call, freq):
    return {
        "ts": "2099-01-01 00:00:00",
        "callsign": call,
        "freq": freq,
        "band": "40",
        "mode": "CW",
        "spotter": "TEST",
        "comment": "",
    }


def test_get_spot_near():
    spots = Database()
    spots.addspot(_spot("DL1AAA", 7020.0))
    spots.addspot(_spot("DL2BBB", 7020.4))
    assert spots.get_spot_near(7020.1, 0.25)["callsign"] == "DL1AAA"
    assert spots.get_spot_near(7020.3, 0.25)["callsign"] == "DL2BBB"
    assert spots.get_spot_near(7021.0, 0.25) is None
