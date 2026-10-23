import os
import requests

def send_slack_notification(task_title):
    slack_token = os.environ.get("SLACK_BOT_TOKEN")

    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={
            "Authorization": f"Bearer {slack_token}"
        },
        json={
            "channel": "task-notifications-c26",
            "text": f"Someone just completed the task {task_title}"
        },
        timeout=10
    )

    response.raise_for_status()
