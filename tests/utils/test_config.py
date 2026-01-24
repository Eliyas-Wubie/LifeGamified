from src.utils.config import load_config

def test_load_config_loads_file():
    config = load_config()
    # Basic sanity checks
    assert isinstance(config, dict)
    assert "base_activities" in config