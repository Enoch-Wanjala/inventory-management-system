import requests


BASE_URL = "https://world.openfoodfacts.org"
HEADERS = {
    "User-Agent": "InventoryManagementStudentProject/1.0 (github.com/Enoch-Wanjala)"
}


def clean_product(product):
    """Keep only the product details used by our inventory."""
    return {
        "product_name": product.get("product_name", "Unknown product"),
        "brands": product.get("brands", ""),
        "ingredients_text": product.get("ingredients_text", ""),
        "barcode": product.get("code", ""),
        "image_url": product.get("image_url", ""),
    }


def get_product_by_barcode(barcode):
    fields = "code,product_name,brands,ingredients_text,image_url"
    url = f"{BASE_URL}/api/v3/product/{barcode}.json"

    try:
        response = requests.get(
            url,
            params={"fields": fields},
            headers=HEADERS,
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError):
        return None

    if not data.get("product"):
        return None
    return clean_product(data["product"])


def search_products_by_name(name):
    # OpenFoodFacts currently uses this endpoint for a simple text search.
    url = f"{BASE_URL}/cgi/search.pl"
    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 5,
    }

    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError):
        return None

    return [clean_product(product) for product in data.get("products", [])]
