from fastapi import APIRouter, Depends, Security, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependepcies import get_session, get_user_service, verify_auth_token
from api.dto.user import SignInUserRequest, SignUpUserRequest
from api.exceptions import UserNotFoundException
from api.services.user import UserService

router = APIRouter(prefix="/users")


@router.post("/sign-in/")
async def sign_in(
    request: SignInUserRequest,
    session: AsyncSession = Depends(get_session),
    service: UserService = Depends(get_user_service),
    _: None = Security(verify_auth_token),
) -> JSONResponse:
    try:
        await service.auth(user_data=request, session=session)
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


@router.post("/sign-up/")
async def sign_up(
    request: SignUpUserRequest,
    session: AsyncSession = Depends(get_session),
    service: UserService = Depends(get_user_service),
    _: None = Security(verify_auth_token),
) -> JSONResponse:
    try:
        result = await service.sign_up(user_data=request, session=session)
    except Exception as exc:
        content = {"success": False, "message": str(exc)}
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        content = {"success": True}
        status_code = result.http_status

    return JSONResponse(
        content=content,
        status_code=status_code,
    )
