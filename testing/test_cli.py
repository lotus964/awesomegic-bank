import pytest
from unittest.mock import patch
from banking.cli import CLI

def test_quit_command_prints_exit_message(capsys):
    with patch("builtins.input", side_effect=["q"]):
        cli = CLI()
        cli.run()
        captured = capsys.readouterr()
        assert "Thank you for banking with AwesomeGIC Bank." in captured.out

def test_invalid_option_shows_error(capsys):
    with patch("builtins.input", side_effect=["x", "q"]):
        cli = CLI()
        cli.run()
        captured = capsys.readouterr()
        assert "Invalid option" in captured.out

def test_handle_transactions_invalid_input(capsys):
    with patch("builtins.input", side_effect=["T", "bad input", "", "q"]):
        cli = CLI()
        cli.run()
        captured = capsys.readouterr()
        assert "Invalid input format" in captured.out

def test_handle_interest_rules_invalid_input(capsys):
    with patch("builtins.input", side_effect=["I", "bad input", "", "q"]):
        cli = CLI()
        cli.run()
        captured = capsys.readouterr()
        assert "Invalid input format" in captured.out
