"""Regicide TUI - Main entry point."""

from src.ui.screens import GameScreen


def main():
    app = GameScreen()
    app.run()


if __name__ == "__main__":
    main()
