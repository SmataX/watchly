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

async def send_data(
    url: str,
    payload: dict,
    client: httpx.AsyncClient,
    method: str = "POST",
    token: Optional[str] = None,
    as_form: bool = False
):
    headers = {}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        request_kwargs = {"data": payload} if as_form else {"json": payload}

        response = await client.request(
            method,
            url,
            headers=headers,
            **request_kwargs
        )

        if response.is_success:
            return response.json()
    except httpx.RequestError:
        return None