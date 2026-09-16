import redis
from app.redis import redis_windows as redis_client
from app.redis_stream import StreamKey

def create_consumer_group(stream_key: StreamKey, group_name: str):
    try:
        redis_client.xgroup_create(
            name=stream_key.value,
            groupname=group_name,
            id="0",
            mkstream=True
        )

        print(f"Created group '{group_name}' for '{stream_key.value}'")

    except redis.exceptions.ResponseError as e:
        if "BUSYGROUP" in str(e):
            print(f"Group '{group_name}' already exists")
        else:
            raise
        
create_consumer_group(
    StreamKey.TASK,
    "task_notifications"
)

create_consumer_group(
    StreamKey.USER,
    "user_notifications"
)
