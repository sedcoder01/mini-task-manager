from enum import Enum
import redis
from app.redis import redis_client

class StreamKey(str,Enum):
    TASK = "task_events"
    USER = "user_events"

class TaskEvents(str,Enum):
    CREATED = 'task_created'
    DELETED = 'task_deleted'
    STATUS_UPDATED = 'task_status_updated'
    PRIORITY_UPDATED = "task_priority_updated"
    DUE_DATE_UPDATED = "task_due_date_updated"
    INFO_UPDATED = "task_info_updated"
    USER_ID_UPDATED = "task_user_id_updated"
    
class UserEvents(str,Enum):
    LOGGED_IN = "logged in"
    CREATED = 'user_created'
    DELETED = 'user_deleted'
    PASSWORD_UPDATED = 'user_password_updated'
    ROLE_UPDATED = "user_role_updated"
    INFO_UPDATED = "user_info_updated"
    
def publish_task_event(
    key: StreamKey,
    event: TaskEvents,
    task_id: int,
    user_id: int
):
    
    return redis_client.xadd(
        key,
        {
            'event': event,
            'task_id': str(task_id),
            'user_id': str(user_id)
        }
    )
    
def publish_user_event(
    key: StreamKey,
        event: UserEvents,
        user_id: int
    ):
        return redis_client.xadd(
            key,
            {
                'event': event,
                'user_id': str(user_id)
            }
        )
