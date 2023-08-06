"""
Login to a Terracomp server.
"""

from typing import Optional

from typer import Option


def main(
    url: str,
    token: Optional[str] = Option(
        None, help="The Terracomp authorization token. If not specified, you will be prompted.", metavar="TOKEN"
    ),
    alias: str = Option("default", help="An alias for the Terracomp server.", metavar="ALIAS"),
    use: bool = Option(True, help="Set this Terracomp server as the default for future invokations."),
) -> None:
    pass
