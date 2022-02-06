import os
from django.http import JsonResponse
import pusher
import json

PUSHER_CLIENT = pusher.Pusher(
    app_id=os.environ.get('ENV_PUSHER_APP_ID'),
    key=os.environ.get('ENV_PUSHER_KEY'),
    secret=os.environ.get('ENV_PUSHER_SECRET'),
    cluster=os.environ.get('ENV_PUSHER_CLUSTER'),
    ssl=True
)


def send_command(command):
    PUSHER_CLIENT.trigger('krill', 'command', {'cmd': command})


def webhook(request):
    data = json.loads(request.body)
    print(data)
    webhook = PUSHER_CLIENT.validate_webhook(
        key=request.headers.get('X-Pusher-Key'),
        signature=request.headers.get('X-Pusher-Signature'),
        body=request.body
    )

    if(webhook is None):
        print('Webhook incorreto')
        return JsonResponse({'msg': 'Webhook incorreto'}, status=400)

    for event in webhook['events']:
        if event['name'] == "channel_occupied":
            print("Channel occupied: %s" % event["channel"])
        elif event['name'] == "channel_vacated":
            print("Channel vacated: %s" % event["channel"])
    print(webhook)

    return JsonResponse({'msg': 'ok'})
