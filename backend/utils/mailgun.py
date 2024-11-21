import requests
from django.conf import settings


def send_mailgun_email(subject, message, to_email, html=None):
    api_url = f"https://api.mailgun.net/v3/{settings.MAILGUN_DOMAIN}/messages"

    auth = ("api", settings.MAILGUN_API_KEY)
    data = {
        "from": f"Stephanie Bee <orders@{settings.MAILGUN_DOMAIN}>",
        "to": to_email,
        "subject": subject,
        "text": message,
    }
    
    if html:
        data["html"] = html

    response = requests.post(api_url, auth=auth, data=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to send email: {response.text}")
