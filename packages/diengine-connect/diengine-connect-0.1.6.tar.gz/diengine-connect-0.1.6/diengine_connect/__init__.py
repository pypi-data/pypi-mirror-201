from diengine_connect.driver import create_client
from diengine_connect.entry_points import validate_entrypoints

driver_name = 'dienginedb'


def get_client(**kwargs):
    return create_client(**kwargs)


def check_ep():
    assert validate_entrypoints() == 0
