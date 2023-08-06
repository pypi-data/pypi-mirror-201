"""
The Terracomp CLI.
"""

import sys
from contextlib import ExitStack
from functools import partial
from pathlib import Path
from typing import Optional

from rich import print
from terracomp_api import TerracompClient
from terracomp_typer import DelayedBinding, DependencyInjector
from typer import Exit, Option

from terracomp_cli.config import DEFAULT_CONFIG_FILE, TerracompConfig, TerracompProfile, load_config

eprint = partial(print, file=sys.stderr)


def callback(
    url: Optional[str] = Option(None, help="The URL to the Terracomp server.", metavar="URL", envvar="TERRACOMP_URL"),
    token: Optional[str] = Option(
        None, help="The authorization token for the Terracomp server.", metavar="TOKEN", envvar="TERRACOMP_TOKEN"
    ),
    profile: Optional[str] = Option(
        None,
        "--profile",
        help="Use the URL and token associated with the specified profile alias.",
        metavar="ALAIS",
        envvar="TERRACOMP_PROFILE",
    ),
    config_file: Path = Option(
        DEFAULT_CONFIG_FILE,
        "--config-file",
        "-c",
        help="Path to the Terracomp configuration file.",
        envvar="TERRACOMP_CONFIG",
    ),
    *,
    dependencies: DependencyInjector = DelayedBinding(TerracompConfig, TerracompClient),
    exit_stack: ExitStack,
) -> None:
    def get_config() -> TerracompConfig:
        if config_file.exists():
            return load_config(config_file)
        else:
            return TerracompConfig()

    def get_profile(config: TerracompConfig) -> TerracompProfile:
        nonlocal profile
        if profile is None:
            profile = config.current_profile
            if profile is None:
                if url is None or token is None:
                    eprint(
                        "[bold red]No Terracomp profile configured, please use [cyan]terracomp login[/cyan] or pass "
                        "[green]--url[/green],[green]--token[/green]"
                    )
                    raise Exit(code=1)
                else:
                    return TerracompProfile(url, token)
            if profile not in config.profiles:
                eprint(f"[bold red]The current Terracomp profile {profile!r} does not exist.[/bold red]")
                raise Exit(code=1)
        elif profile not in config.profiles:
            eprint(f"[bold red]The Terracomp profile {profile!r} does not exist.[/bold red]")
            raise Exit(code=1)
        return TerracompProfile(
            url=url or config.profiles[profile].url,
            token=token or config.profiles[profile].token,
        )

    def create_client(profile: TerracompProfile) -> TerracompClient:
        client = TerracompClient.from_url(profile.url, profile.token)
        exit_stack.callback(client.close)
        return client

    dependencies.register_supplier(TerracompConfig, get_config)
    dependencies.register_supplier(TerracompProfile, get_profile)
    dependencies.register_supplier(TerracompClient, create_client)
