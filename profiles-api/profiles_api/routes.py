from uuid import UUID

from fastapi import APIRouter

from profiles_api.factories import UserProfileFactory
from profiles_api.schemas import UserProfile, UserProfilesPage

router = APIRouter()


@router.get("/profiles/{user_id}", response_model=UserProfile)
def get_user_profile(user_id: UUID) -> UserProfile:
    return UserProfileFactory.build(user_id=user_id)


@router.get("/groups/{group_id}/profiles", response_model=UserProfilesPage)
def get_user_profiles_for_group(group_id: UUID) -> UserProfilesPage:  # noqa: ARG001
    num_users = 10
    return UserProfilesPage(
        profiles=UserProfileFactory.batch(num_users), total=num_users, page=1, size=50, pages=1
    )
