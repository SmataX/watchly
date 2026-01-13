from fastapi import APIRouter
from src.modules.auth.deps import UserDep
from .deps import FollowOperationsDep
from .schemes import FollowScheme

router = APIRouter(prefix="/follow", tags=['Follows'])

@router.post("/")
def follow(follow_ops: FollowOperationsDep, user: UserDep, form: FollowScheme):
    return follow_ops.add(form.user_id, form.follow_id)

@router.delete("/")
def unfollow(follow_ops: FollowOperationsDep, user: UserDep, form: FollowScheme):
    return follow_ops.remove(form.user_id, form.follow_id)

@router.get("/{id}")
def get_all_for_user(follow_ops: FollowOperationsDep, id: int):
    return follow_ops.get_all_for_user(id)