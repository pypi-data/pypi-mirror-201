"""
List available projects.
"""

from terracomp_api import TerracompClient


async def main(client: TerracompClient) -> None:
    print(">>> ls")
    print(await client.list_projects())
    pass
