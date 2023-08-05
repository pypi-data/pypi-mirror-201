"""
Run the CLI application
"""
from sempyver import CLI


def run() -> None:
    """Run the CLI application"""
    cli_app = CLI()
    app = cli_app.generate()
    # Run the app
    app()


if __name__ == "__main__":
    run()
