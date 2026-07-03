from unittest.mock import Mock, patch

import requests

from openfoodfacts import get_product_by_barcode, search_products_by_name


def test_get_product_by_barcode():
    fake_response = Mock()
    fake_response.json.return_value = {
        "product": {
            "code": "123",
            "product_name": "Chocolate",
            "brands": "Test",
            "ingredients_text": "Cocoa and sugar",
        }
    }

    with patch("openfoodfacts.requests.get", return_value=fake_response):
        product = get_product_by_barcode("123")

    assert product["product_name"] == "Chocolate"
    assert product["barcode"] == "123"


def test_product_api_failure():
    with patch(
        "openfoodfacts.requests.get",
        side_effect=requests.RequestException,
    ):
        product = get_product_by_barcode("123")

    assert product is None


def test_search_products_by_name():
    fake_response = Mock()
    fake_response.json.return_value = {
        "products": [{"code": "456", "product_name": "Oat Milk"}]
    }

    with patch("openfoodfacts.requests.get", return_value=fake_response):
        products = search_products_by_name("oat milk")

    assert len(products) == 1
    assert products[0]["product_name"] == "Oat Milk"
