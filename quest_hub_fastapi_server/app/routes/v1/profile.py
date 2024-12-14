from fastapi import APIRouter, Depends

from quest_hub_fastapi_server.modules.profile import get_profile
from quest_hub_fastapi_server.modules.profile import Profile
from quest_hub_fastapi_server.modules.profile.models import RequestProfileModel


profile_route = APIRouter(tags=["profile"])


@profile_route.post(path="/profile")
def create_user(
    rq_profile_model: RequestProfileModel,
    profile: Profile = Depends(get_profile),
):
    return profile.create_or_update(rq_profile_model)


@profile_route.put(path="/profile")
def edit_user(
    rq_profile_model: RequestProfileModel,
    profile: Profile = Depends(get_profile),
):
    return profile.create_or_update(rq_profile_model)


@profile_route.get(path="/profile")
def get_user(tg_id: int, profile: Profile = Depends(get_profile)):
    return profile.get_by_tg_id(tg_id)


@profile_route.delete(path="/profile")
def delete_user(tg_id: int, profile: Profile = Depends(get_profile)):
    return profile.delete(tg_id)
