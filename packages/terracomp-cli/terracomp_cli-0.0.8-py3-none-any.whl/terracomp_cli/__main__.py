from contextlib import ExitStack

from terracomp_typer import build_app_from_module


def main() -> None:
    with ExitStack() as exit_stack:
        app = build_app_from_module(
            module_name="terracomp_cli.commands",
            typer_options=dict(no_args_is_help=True, rich_markup_mode="rich", pretty_exceptions_enable=False),
            dependencies=[exit_stack],
        )
        app()


if __name__ == "__main__":
    main()
