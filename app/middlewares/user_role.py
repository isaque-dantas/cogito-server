from fastapi import Request, HTTPException, Depends

from app.services.auth import AuthService

from typing import Annotated
from app.models import User, UserRoles


class UserRoleMiddleware:
    def __init__(self, roles_who_can_access: list[str]):
        self.roles_who_can_access = roles_who_can_access

    async def __call__(self, request: Request, token: str = Depends(AuthService.mandatory_oauth2_scheme)):
        current_user: User = await AuthService.get_mandatory_current_user(token)

        if current_user.role not in self.roles_who_can_access:
            raise HTTPException(
                status_code=403,
                detail="Not authorized to access this resource",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return current_user


coordinator_only_middleware = UserRoleMiddleware([UserRoles.coordinator])
CoordinatorOnlyDependency = Depends(coordinator_only_middleware)
CoordinatorLogged = Annotated[User, Depends(coordinator_only_middleware)]
