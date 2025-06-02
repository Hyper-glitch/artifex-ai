from fastapi import APIRouter, Depends, Security, status
from fastapi.responses import JSONResponse

from api.dto.task import UpdateTaskRequest, UpdateTaskResponse

worker_router = APIRouter(prefix="/worker")


@worker_router.post("/tasks/update/")
async def update_task(
    request: UpdateTaskRequest,
    task_service: MLTaskService = Depends(get_ml_task_service),
    worker_key: str = Security(verify_worker_access),
) -> UpdateTaskResponse:
    try:
        task_id = await task_service.update_task(request)
    except Exception as exc:
        return JSONResponse(
            content={"success": False, "message": str(exc)},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return UpdateTaskResponse(task_id=task_id)
