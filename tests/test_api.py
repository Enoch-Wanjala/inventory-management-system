from unittest.mock import patch

from app import inventory


def test_get_all_inventory(client):
    response = client.get("/inventory")

    assert response.status_code == 200
    assert len(response.get_json()) == 1


def test_get_one_item(client):
    response = client.get("/inventory/1")

    assert response.status_code == 200
    assert response.get_json()["product_name"] == "Test Milk"


def test_get_missing_item(client):
    response = client.get("/inventory/99")

    assert response.status_code == 404


def test_add_item(client):
    response = client.post(
        "/inventory",
        json={"product_name": "Bread", "price": 2.50, "stock": 6},
    )

    assert response.status_code == 201
    assert response.get_json()["id"] == 2
    assert len(inventory) == 2


def test_add_item_requires_name(client):
    response = client.post("/inventory", json={"stock": 4})

    assert response.status_code == 400


def test_update_item(client):
    response = client.patch("/inventory/1", json={"price": 5, "stock": 20})

    assert response.status_code == 200
    assert response.get_json()["stock"] == 20


def test_delete_item(client):
    response = client.delete("/inventory/1")

    assert response.status_code == 200
    assert inventory == []


def test_barcode_lookup_route(client):
    product = {"product_name": "API Milk", "barcode": "123456"}

    with patch("app.get_product_by_barcode", return_value=product):
        response = client.get("/products/barcode/123456")

    assert response.status_code == 200
    assert response.get_json()["product_name"] == "API Milk"


def test_import_product(client):
    product = {
        "product_name": "API Milk",
        "brands": "API Brand",
        "ingredients_text": "Milk",
        "barcode": "123456",
        "image_url": "",
    }

    with patch("app.get_product_by_barcode", return_value=product):
        response = client.post("/inventory/import/123456")

    assert response.status_code == 201
    assert response.get_json()["id"] == 2
    assert len(inventory) == 2
