import json
from unittest.mock import Mock

import procedures


def test_print_formats_a_current_timestamp(capsys):
    line = procedures.print_(["clock regression"])
    assert "clock regression" in line
    assert line in capsys.readouterr().out


def test_fresh_eligible_symbols_cache_does_not_fetch(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    cache_dir = tmp_path / "caches" / "binance"
    cache_dir.mkdir(parents=True)
    (cache_dir / "eligible_symbols.json").write_text(json.dumps(["BTCUSDT", "ETHUSDT"]))

    import ccxt

    exchange_factory = Mock(side_effect=AssertionError("A fresh cache must not instantiate an exchange client"))
    monkeypatch.setattr(ccxt, "binanceusdm", exchange_factory)
    assert procedures.get_all_eligible_symbols("binance") == ["BTCUSDT", "ETHUSDT"]
    exchange_factory.assert_not_called()
