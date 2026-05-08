from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.db.models.user import User
from app.db.models.task import Task
from app.schemas.task import ShareRequest
from app.services.email_service import send_task_list_email

router = APIRouter(prefix="/tasks", tags=["sharing"])


@router.post("/share")
def share_tasks(
    payload: ShareRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tasks = db.query(Task).filter(Task.owner_id == current_user.id).all()
    if not tasks:
        raise HTTPException(status_code=400, detail="You have no tasks to share")
    try:
        send_task_list_email(
            to_email=payload.email,
            tasks=tasks,
            from_user_email=current_user.email,
        )
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to send email. Check SMTP settings.")
    return {"detail": f"Task list sent to {payload.email}"}
