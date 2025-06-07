import logging
from fastapi.responses import JSONResponse

from fastapi import APIRouter, Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.dependepcies import get_session, verify_auth_token, get_task_service
from api.dto.task import AITaskRequest, UpdateTaskRequest
from api.services.task import TaskService

router = APIRouter(prefix="/tasks")


@router.post("/create/")
async def create(
    request: AITaskRequest,
    session: AsyncSession = Depends(get_session),
    service: TaskService = Depends(get_task_service),
    _: None = Security(verify_auth_token),
) -> JSONResponse:
    try:
        await service.create(task_data=request, session=session)
    except Exception as exc:
        logging.warning(f"Problem when creating AI task {request.task_id}")
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        content = {"success": False, "message": str(exc)}
    else:
        content = {"success": True}
        status_code = status.HTTP_200_OK

    return JSONResponse(
        content=content,
        status_code=status_code,
    )


@router.post("/update/")
async def update(
    request: UpdateTaskRequest,
    session: AsyncSession = Depends(get_session),
    service: TaskService = Depends(get_task_service),
    _: None = Security(verify_auth_token),
) -> JSONResponse:
    try:
        await service.update(task_data=request, session=session)
    except Exception as exc:
        logging.warning(f"Problem when updating AI task {request.task_id}")
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        content = {"success": False, "message": str(exc)}
    else:
        content = {"success": True}
        status_code = status.HTTP_200_OK

    return JSONResponse(
        content=content,
        status_code=status_code,
    )
