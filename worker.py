import sys
import redis

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
    socket_timeout=None
)

user_id = int(sys.argv[1])
stream_key = f'user:{user_id}:notifications'
last_read_key = f'user:{user_id}:notifications:last_read'
last_id = redis_client.get(last_read_key) or '0-0'
# pubsub = redis_client.pubsub()
# pubsub.subscribe(channel)
print(f"Listening for notifications for user {user_id}...")
while True:
    messages = redis_client.xread(
        {stream_key: last_id},
        block=0
    )
    for stream, entries in messages:
        for message_id, data in entries:
            print(f'🔔 {data["message"]}')
            last_id = message_id
            redis_client.set(last_read_key, last_id)
# for message in pubsub.listen():
#     if message['type'] == 'message':
#         print(f'🔔 {message["data"]}')