import os
from slack_sdk.webhook import WebhookClient


slack_webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
webhook = WebhookClient(slack_webhook_url)

def send_success_notify(context):
    dag_id = context['task_instance'].dag_id
    execution_date = context['execution_date']
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
                    "text": f"*DAG ID:* {dag_id}\n*Notification*: ✅ Dag Success\n*Execution Date:* {execution_date}"
                }
            },        
            {
                "type": "divider"
            },
        ]
    )

def send_failed_notiy(context):
    dag_id = context['task_instance'].dag_id
    task_id = context['task_instance'].task_id
    execution_date = context['execution_date']
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
                    "text": f"""*DAG ID:* {dag_id}\n
                        *Task ID:* {task_id}\n
                        *Notification*: ❌ Dag Validation Failed
                        \n*Execution Date:* {execution_date}"""
                }
            },        
            {
                "type": "divider"
            },
        ]
    )
