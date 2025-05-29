from exceptions import UserNotFoundException
from fastapi import APIRouter, Depends, Security, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependepcies import get_auth_service, get_session, verify_auth_token
from api.dto.user import AuthUserRequest
from api.services.auth import AuthService

router = APIRouter(prefix="/users")


@router.post("/authorize/")
async def authorize(
    request: AuthUserRequest,
    session: AsyncSession = Depends(get_session),
    auth_service: AuthService = Depends(get_auth_service),
    _: None = Security(verify_auth_token),
) -> JSONResponse:
    try:
        await auth_service.auth_user(user_data=request, session=session)
    except UserNotFoundException as exc:
        status_code = status.HTTP_400_BAD_REQUEST
        content = {"success": False, "message": str(exc)}
    else:
        content = {"success": True}
        status_code = status.HTTP_200_OK

    return JSONResponse(
        content=content,
        status_code=status_code,
    )
