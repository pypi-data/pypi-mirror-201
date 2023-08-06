"""
Spin up a local Terracomp server.
"""


async def main(host: str = "localhost", port: int = 7331) -> None:
    from terracomp_server import start_server

    print(f"Starting Terracomp server at {host}:{port}")
    await start_server(host=host, port=port)
