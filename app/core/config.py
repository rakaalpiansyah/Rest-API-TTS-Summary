"""
Konfigurasi sentral aplikasi.
Semua env variable dibaca dari sini — satu sumber kebenaran.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    # ── App ──────────────────────────────────────────────────
    app_name: str = "Meeting AI Backend"
    app_version: str = "1.0.0"
    debug: bool = False
    secret_key: str = "changeme"

    # ── AI ───────────────────────────────────────────────────
    gemini_api_key: str
    whisper_model_size: str = "base"  # tiny/base/small/medium/large

    # ── Supabase ─────────────────────────────────────────────
    supabase_url: str
    supabase_anon_key: str
    supabase_service_role_key: str

    # ── CORS ─────────────────────────────────────────────────
    frontend_url: str = "http://localhost:5173"
    allowed_origins: str = ""  # comma-separated, isi saat production

    def get_allowed_origins(self) -> List[str]:
        """
        Gabungkan semua allowed origins.
        Localhost selalu diizinkan untuk development.
        """
        origins = [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
            self.frontend_url,
        ]
        # Tambah origins dari env jika ada (comma-separated)
        if self.allowed_origins:
            extras = [o.strip() for o in self.allowed_origins.split(",") if o.strip()]
            origins.extend(extras)
        # Buang duplikat
        return list(set(origins))

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Cached settings — hanya dibaca sekali dari disk.
    Gunakan dependency injection FastAPI untuk akses di endpoint.
    """
    return Settings()