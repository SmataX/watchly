from fastapi import APIRouter
from src.modules.auth.deps import UserDep
from src.modules.user.deps import UserOperationsDep
from .deps import FollowOperationsDep
from .schemes import FollowScheme

router = APIRouter(prefix="/follow", tags=['Follows'])

@router.post("/")
def follow(follow_ops: FollowOperationsDep, users_ops: UserOperationsDep, user: UserDep, form: FollowScheme):
    return follow_ops.add(user['id'], users_ops.get_user_by_username(form.username).id)

@router.delete("/")
def unfollow(follow_ops: FollowOperationsDep, users_ops: UserOperationsDep, user: UserDep, form: FollowScheme):
    print(form.username)
    return follow_ops.remove(user['id'], users_ops.get_user_by_username(form.username).id)

@router.get("/{id}")
def get_all_for_user(follow_ops: FollowOperationsDep, id: int):
    return follow_ops.get_all_for_user(id)

@router.get("/follow/{username}")
def is_following(follow_ops: FollowOperationsDep, username: str, user: UserDep, users_ops: UserOperationsDep):
    target_user = users_ops.get_user_by_username(username)
    if not target_user:
        return False
        
    return follow_ops.is_followed(user['id'], target_user.id)