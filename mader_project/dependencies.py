from typing import Annotated

from fastapi import Depends

from mader_project.database import AsyncSession, get_session
from mader_project.models import User
from mader_project.security import get_current_user, get_password_hash

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]