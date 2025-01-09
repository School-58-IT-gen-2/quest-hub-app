from fastapi import APIRouter, HTTPException

from quest_hub_fastapi_server.modules.profile import Profile
from quest_hub_fastapi_server.modules.settings import settings
from quest_hub_fastapi_server.adapters.db_source import DBSource
from quest_hub_fastapi_server.modules.profile.models import (
    ProfileRequest,
    ProfilePutRequest,
)


status_route = APIRouter(prefix="/status", tags=["app_status"])


@status_route.get(path="/health")
def health():
    new_db_source = DBSource(settings.supabase.url, settings.supabase.key)
    new_db_source.connect()
    return {"status": "ok"}