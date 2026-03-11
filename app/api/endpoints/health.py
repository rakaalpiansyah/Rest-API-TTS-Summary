"""
Health Check Endpoint.
Digunakan untuk monitoring dan deployment checks (Docker, K8s, dll).
"""
from fastapi import APIRouter
from app.core.config import get_settings

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    """Cek status server dan model AI."""
    settings = get_settings()

    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version,
        "services": {
            "whisper": "groq_api" if settings.groq_api_key else "missing_api_key",
            "ai": "configured" if settings.gemini_api_key else "missing_api_key",
            "supabase": "configured" if settings.supabase_url else "missing_url",
        },
    }