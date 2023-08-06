"""wee"""

band_indicators_cw = {
    "160": "cw_band_160",
    "80": "cw_band_80",
    "40": "cw_band_40",
    "20": "cw_band_20",
    "15": "cw_band_15",
    "10": "cw_band_10",
}

band_indicators_ssb = {
    "160": "ssb_band_160",
    "80": "ssb_band_80",
    "40": "ssb_band_40",
    "20": "ssb_band_20",
    "15": "ssb_band_15",
    "10": "ssb_band_10",
}

band_indicators_rtty = {
    "160": "rtty_band_160",
    "80": "rtty_band_80",
    "40": "rtty_band_40",
    "20": "rtty_band_20",
    "15": "rtty_band_15",
    "10": "rtty_band_10",
}

all_mode_indicators = {
    "CW": band_indicators_cw,
    "SSB": band_indicators_ssb,
    "RTTY": band_indicators_rtty,
}

for mode, indicators in all_mode_indicators.items():
    print(f"clear band indicators mode: {mode}")
    for band, indicator in indicators.items():
        print(f"band item: {indicator}")
