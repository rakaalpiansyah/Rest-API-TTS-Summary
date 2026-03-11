"""
API Key Authentication — Middleware sederhana.
Client harus kirim header `X-API-Key` yang cocok dengan salah satu key di env.
Health check TIDAK perlu API key.
"""
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from app.core.config import get_settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header)):
    """
    Dependency FastAPI — cek header X-API-Key.
    Jika tidak valid, return 401 Unauthorized.
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key diperlukan. Kirim header 'X-API-Key'.",
        )

    settings = get_settings()
    valid_keys = settings.get_api_keys()

    if api_key not in valid_keys:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key tidak valid.",
        )

    return api_key
