from flask import Flask, jsonify, request


app = Flask(__name__)

# This list acts as our temporary database.
inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar",
        "barcode": "025293600270",
        "price": 4.50,
        "stock": 10,
    },
    {
        "id": 2,
        "product_name": "Corn Flakes",
        "brands": "Kellogg's",
        "ingredients_text": "Milled corn, sugar, salt",
        "barcode": "038000001109",
        "price": 3.25,
        "stock": 18,
    },
]


@app.route("/")
def home():
    return jsonify({"message": "Inventory Management API"})


@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory)


@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = find_item(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item)


@app.route("/inventory", methods=["POST"])
def add_item():
    data = request.get_json(silent=True)
    if not data or not data.get("product_name"):
        return jsonify({"error": "product_name is required"}), 400

    new_id = max([item["id"] for item in inventory], default=0) + 1
    new_item = {
        "id": new_id,
        "product_name": data["product_name"],
        "brands": data.get("brands", ""),
        "ingredients_text": data.get("ingredients_text", ""),
        "barcode": data.get("barcode", ""),
        "price": data.get("price", 0),
        "stock": data.get("stock", 0),
    }
    inventory.append(new_item)
    return jsonify(new_item), 201


@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    item = find_item(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No update data provided"}), 400

    allowed_fields = [
        "product_name", "brands", "ingredients_text",
        "barcode", "price", "stock"
    ]
    for field in allowed_fields:
        if field in data:
            item[field] = data[field]

    return jsonify(item)


@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = find_item(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404

    inventory.remove(item)
    return jsonify({"message": "Item deleted"})


def find_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return item
    return None


if __name__ == "__main__":
    app.run(debug=True)
