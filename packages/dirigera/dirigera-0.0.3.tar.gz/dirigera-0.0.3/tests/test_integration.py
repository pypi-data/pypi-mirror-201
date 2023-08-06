import os
import pytest
from src import dirigera


@pytest.fixture(name="dirigera_hub")
def fixture_hub():
    return dirigera.Hub(
        token=os.getenv("DIRIGERA_TOKEN"), ip_address=os.getenv("DIRIGERA_IP_ADDRESS")
    )


def test_hub(dirigera_hub: dirigera.Hub):
    lights = dirigera_hub.get_lights()
    assert len(lights) > 0
    sensors = dirigera_hub.get_environment_sensors()
    assert len(sensors) > 0
