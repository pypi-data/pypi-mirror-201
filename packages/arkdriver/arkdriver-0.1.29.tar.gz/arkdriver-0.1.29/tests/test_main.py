import arkdriver

def test_imports():
    arkdriver.main.__testing__ = True
    try:
        from arkdriver import run
    except Exception:
        print()
        assert False, arkdriver.console.error("Cannot import run from arkdriver.")
    arkdriver.main.__testing__ = False


def test_run():
    arkdriver.main.__testing__ = True
    from arkdriver import run
    try:
        run()
    except Exception as e:
        print()
        assert False, arkdriver.console.error(f"Function run() from main failed: {e}")
    arkdriver.main.__testing__ = False

