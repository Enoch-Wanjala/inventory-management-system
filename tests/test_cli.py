from unittest.mock import Mock, patch

import requests

from cli import build_parser, run_command


def run_cli(arguments):
    args = build_parser().parse_args(arguments)
    run_command(args)


def test_cli_list(capsys):
    fake_response = Mock()
    fake_response.json.return_value = [{"id": 1, "product_name": "Milk"}]

    with patch("cli.requests.request", return_value=fake_response) as request:
        run_cli(["list"])

    request.assert_called_once()
    assert "Milk" in capsys.readouterr().out


def test_cli_add():
    fake_response = Mock()
    fake_response.json.return_value = {"id": 2, "product_name": "Bread"}

    with patch("cli.requests.request", return_value=fake_response) as request:
        run_cli(["add", "Bread", "--price", "2.5", "--stock", "4"])

    sent_data = request.call_args.kwargs["json"]
    assert request.call_args.args[0] == "POST"
    assert sent_data["product_name"] == "Bread"


def test_cli_update():
    fake_response = Mock()
    fake_response.json.return_value = {"id": 1, "stock": 15}

    with patch("cli.requests.request", return_value=fake_response) as request:
        run_cli(["update", "1", "--stock", "15"])

    assert request.call_args.args[0] == "PATCH"
    assert request.call_args.kwargs["json"] == {"stock": 15}


def test_cli_delete():
    fake_response = Mock()
    fake_response.json.return_value = {"message": "Item deleted"}

    with patch("cli.requests.request", return_value=fake_response) as request:
        run_cli(["delete", "1"])

    assert request.call_args.args[0] == "DELETE"


def test_cli_connection_error(capsys):
    with patch("cli.requests.request", side_effect=requests.RequestException):
        run_cli(["list"])

    assert "Could not connect" in capsys.readouterr().out
