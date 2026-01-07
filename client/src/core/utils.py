import httpx

async def get_data(url: str, client):
    try:
        response = await client.get(url)

        if response.status_code == 200:
            return(response.json())
    except httpx.RequestError:
        return None