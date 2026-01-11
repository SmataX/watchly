import httpx
from typing import Optional

async def get_data(url: str, client, token: Optional[str] = None):
    headers = {}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        response = await client.get(url, headers=headers)

        if response.status_code == 200:
            return(response.json())
    except httpx.RequestError:
        return None