import httpx
from typing import Optional
from fastapi import Request, Depends
from src.settings import settings

async def get_http_client(request: Request) -> httpx.AsyncClient:
    """
    Dependency to retrieve the shared HTTP client from app state.
    """
    return request.app.state.http_client


async def get_optional_user(
    request: Request, 
    client: httpx.AsyncClient = Depends(get_http_client)
) -> Optional[dict]:
    """
    Dependency that attempts to fetch the current user based on cookies.
    
    Args:
        request: The incoming HTTP request containing cookies.
        client: The shared HTTPX client.

    Returns:
        dict: The user data if the token is valid.
        None: If no token exists or the backend rejects the token.
    """
    token = request.cookies.get("access_token")
    if not token:
        return None

    try:
        response = await client.get(
            "/auth/get-user", 
            headers={"Authorization": token}
        )
        if response.status_code == 200:
            return response.json()
    except httpx.RequestError:
        # Log error here in a real app
        pass
        
    return None