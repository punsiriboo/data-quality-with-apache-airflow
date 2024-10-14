import os
from slack_sdk.webhook import WebhookClient


slack_webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
webhook = WebhookClient(slack_webhook_url)

def send_success_notify():
    response = webhook.send(
        text="fallback",
        blocks=[
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Notification*: ✅ Dag Success"
                }
            },        
            {
                "type": "divider"
            },
        ]
    )

def send_fail_notiy():
    response = webhook.send(
        text="fallback",
        blocks=[
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Notification*: ❌ Dag Validation Failed"
                }
            },        
            {
                "type": "divider"
            },
        ]
    )
