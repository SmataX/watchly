from typing import Annotated, Optional
from fastapi import Depends
from .services import get_current_user, get_optional_user

UserDep = Annotated[dict, Depends(get_current_user)]
UserOptionalDep = Annotated[Optional[dict], Depends(get_optional_user)]