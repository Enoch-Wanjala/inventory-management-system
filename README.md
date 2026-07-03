# Inventory Management System

This is a beginner-friendly inventory management project made with Flask. It
allows employees to add, view, update, and delete products. Product information
can also be found and imported from OpenFoodFacts.

The inventory is stored in a Python list, so changes are temporary and reset
when the Flask server restarts.

## Problem and plan

A small shop needs a simple way to manage its stock. The system has three parts:

1. A Flask REST API that manages the inventory list.
2. An OpenFoodFacts connection that searches for real product information.
3. A command-line interface (CLI) that employees can use without Postman.

The API receives JSON input, changes or reads the inventory list, and returns
JSON output. The CLI sends requests to these routes when the user runs a
command.

## Route design

| Method | Route | Input | Result |
| --- | --- | --- | --- |
| GET | `/inventory` | None | Returns all inventory items |
| GET | `/inventory/<id>` | Item ID in the URL | Returns one item |
| POST | `/inventory` | Product JSON | Adds an item to the list |
| PATCH | `/inventory/<id>` | Fields to update as JSON | Updates an item |
| DELETE | `/inventory/<id>` | Item ID in the URL | Deletes an item |
| GET | `/products/barcode/<barcode>` | Barcode in the URL | Finds a product on OpenFoodFacts |
| GET | `/products/search?name=milk` | Product name query | Finds up to five products |
| POST | `/inventory/import/<barcode>` | Barcode in the URL | Imports a product into inventory |

Every inventory item has an ID, product name, brand, ingredients, barcode,
price, and stock level. Imported products can also have an image URL.

## Installation

Clone the project and enter its folder:

```bash
git clone https://github.com/Enoch-Wanjala/inventory-management-system.git
cd inventory-management-system
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

On macOS or Linux:

```bash
source venv/bin/activate
```

Install the packages:

```bash
pip install -r requirements.txt
```

## Run the API

```bash
python app.py
```

The API runs at `http://127.0.0.1:5000`. Flask debug mode is enabled when the
file is run directly, which makes development errors easier to see.

## Example API requests

Add an item with JSON like this in Postman:

```json
{
  "product_name": "Orange Juice",
  "brands": "Example Brand",
  "barcode": "123456789",
  "price": 3.5,
  "stock": 12
}
```

Send it as a `POST` request to `http://127.0.0.1:5000/inventory`.

To update only the stock, send a `PATCH` request to `/inventory/1`:

```json
{
  "stock": 20
}
```

Postman can also be used to try each route in the table. Select the correct
method, enter the URL, and use **Body > raw > JSON** for POST and PATCH data.

## CLI usage

Keep the Flask API running in one terminal. Open a second terminal in the same
folder and use these commands:

```bash
# View all items
python cli.py list

# View one item
python cli.py view 1

# Add an item
python cli.py add "Orange Juice" --brand "Example" --price 3.5 --stock 12

# Update price or stock
python cli.py update 1 --price 4.0 --stock 15

# Delete an item
python cli.py delete 1

# Find an OpenFoodFacts product
python cli.py find --barcode 3017620422003
python cli.py find --name "oat milk"

# Import a product, then update its price and stock
python cli.py import-product 3017620422003
```

Run `python cli.py --help` to see all available commands.

## Tests

Run the tests with:

```bash
pytest -q
```

The tests cover the GET, POST, PATCH, and DELETE routes, CLI commands, and
OpenFoodFacts interactions. External requests are mocked, so the tests do not
change OpenFoodFacts data or depend on an internet connection.

## External API note

This project reads public information from the
[OpenFoodFacts API](https://openfoodfacts.github.io/openfoodfacts-server/api/).
OpenFoodFacts data is community-provided and may sometimes be incomplete. The
application shows a clear error when a product cannot be found or the external
service is unavailable.
