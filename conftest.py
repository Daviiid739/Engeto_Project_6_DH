import pytest

# --- FIXTURES ---
@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Nastaví argumenty pro spuštění browseru — viditelný režim se zpomaleným během."""
    return {
        **browser_type_launch_args,
        "slow_mo": 1000,
        "headless": False
    }

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Nastaví kontext browseru — rozlišení Full HD a české prostředí."""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "cs-CZ",
    }
