from copy import deepcopy

import pytest

from app import app, inventory


SAMPLE_INVENTORY = [
    {
        "id": 1,
        "product_name": "Test Milk",
        "brands": "Test Brand",
        "ingredients_text": "Water and almonds",
        "barcode": "123456",
        "price": 4.50,
        "stock": 10,
    }
]


@pytest.fixture(autouse=True)
def reset_inventory():
    inventory[:] = deepcopy(SAMPLE_INVENTORY)
    yield
    inventory[:] = deepcopy(SAMPLE_INVENTORY)


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()
