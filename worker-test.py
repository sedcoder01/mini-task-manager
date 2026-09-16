import redis
import sys

client = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True,
    socket_timeout=None
)

STREAM_NAME = sys.argv[2]
GROUP_NAME = sys.argv[3]
CONSUMER = sys.argv[1]
print(CONSUMER)

next_id, messages, deleted = client.xautoclaim(
    name=STREAM_NAME,
    groupname=GROUP_NAME,
    consumername=CONSUMER,
    min_idle_time=5000,
    start_id=0,
    count=10
)

print("Next ID: ", next_id)
print("Messages: ", messages)
print("Deleted: ", deleted)
for message_id, data in messages:

    try:
        print("Recovered:", data)
        print("Processing...")

        # پردازش واقعی پیام اینجا

        client.xack(
            STREAM_NAME,
            GROUP_NAME,
            message_id
        )

        print("ACK:", message_id)

    except Exception as e:
        print("Processing failed:", e)

while True:
    messages = client.xreadgroup(
        groupname=GROUP_NAME,
        consumername=CONSUMER,
        streams={STREAM_NAME: ">"},
        block=0
    )
    for stream_name, stream_messages in messages:
        for message_id, data in stream_messages:
            try:
                print("Received:", data)
                print("Processing...")

                user_id = data["user_id"]
                message = f'User {user_id} - Task {data["task_id"]}: {data["event"]}'
                client.xadd(f"user:{user_id}:notifications", {'message': message})
                client.xack(
                    STREAM_NAME,
                    GROUP_NAME,
                    message_id
                )
                print("ACK:", message_id)
                print(message)
                
            except Exception as e:
                print("Processing failed:", e)