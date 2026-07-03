import argparse
import json

import requests


API_URL = "http://127.0.0.1:5000"


def show_response(response):
    try:
        data = response.json()
    except ValueError:
        print("The server returned an invalid response.")
        return

    print(json.dumps(data, indent=2))


def send_request(method, path, data=None):
    try:
        response = requests.request(
            method,
            API_URL + path,
            json=data,
            timeout=10,
        )
        show_response(response)
    except requests.RequestException:
        print("Could not connect to the API. Start it with: python app.py")


def build_parser():
    parser = argparse.ArgumentParser(description="Inventory Management CLI")
    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser("list", help="View all inventory items")

    view = commands.add_parser("view", help="View one inventory item")
    view.add_argument("id", type=int)

    add = commands.add_parser("add", help="Add an inventory item")
    add.add_argument("name")
    add.add_argument("--brand", default="")
    add.add_argument("--barcode", default="")
    add.add_argument("--price", type=float, default=0)
    add.add_argument("--stock", type=int, default=0)

    update = commands.add_parser("update", help="Update price or stock")
    update.add_argument("id", type=int)
    update.add_argument("--price", type=float)
    update.add_argument("--stock", type=int)

    delete = commands.add_parser("delete", help="Delete an inventory item")
    delete.add_argument("id", type=int)

    find = commands.add_parser("find", help="Find products on OpenFoodFacts")
    find_group = find.add_mutually_exclusive_group(required=True)
    find_group.add_argument("--barcode")
    find_group.add_argument("--name")

    import_command = commands.add_parser(
        "import-product", help="Import an OpenFoodFacts product by barcode"
    )
    import_command.add_argument("barcode")

    return parser


def run_command(args):
    if args.command == "list":
        send_request("GET", "/inventory")
    elif args.command == "view":
        send_request("GET", f"/inventory/{args.id}")
    elif args.command == "add":
        item = {
            "product_name": args.name,
            "brands": args.brand,
            "barcode": args.barcode,
            "price": args.price,
            "stock": args.stock,
        }
        send_request("POST", "/inventory", item)
    elif args.command == "update":
        changes = {}
        if args.price is not None:
            changes["price"] = args.price
        if args.stock is not None:
            changes["stock"] = args.stock
        if not changes:
            print("Please provide --price or --stock.")
            return
        send_request("PATCH", f"/inventory/{args.id}", changes)
    elif args.command == "delete":
        send_request("DELETE", f"/inventory/{args.id}")
    elif args.command == "find":
        if args.barcode:
            send_request("GET", f"/products/barcode/{args.barcode}")
        else:
            try:
                response = requests.get(
                    API_URL + "/products/search",
                    params={"name": args.name},
                    timeout=10,
                )
                show_response(response)
            except requests.RequestException:
                print("Could not connect to the API. Start it with: python app.py")
    elif args.command == "import-product":
        send_request("POST", f"/inventory/import/{args.barcode}")


def main():
    parser = build_parser()
    args = parser.parse_args()
    run_command(args)


if __name__ == "__main__":
    main()
