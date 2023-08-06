import arkdriver
from pathlib import Path


def test_configuration():
    path = Path(__file__).parent.parent / Path("tox.ini")
    try:
        config = arkdriver.lib.configuration.Configuration(path)
    except Exception:
        print()
        assert False, arkdriver.console.error(f"Unable to read tox.ini in path: {path}")

