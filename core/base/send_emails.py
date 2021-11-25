import logging

import requests
from celery import shared_task
from django.conf import settings
from requests.auth import HTTPBasicAuth

logger = logging.getLogger("django")


def _send_template_email(
        public_key,
        private_key,
        to_email,
        to_name,
        template_id,
        variables,
):
    url = "https://api.mailjet.com/v3.1/send"
    auth = HTTPBasicAuth(public_key, private_key)
    data = {
        "Messages": [
            {
                "To": [{"Email": to_email, "Name": to_name}],
                "TemplateID": template_id,
                "TemplateLanguage": True,
                "Variables": variables,
            }
        ]
    }
    logger.info(f"Email data: {data}")
    response = requests.post(url=url, json=data, auth=auth)
    return "{}: {}".format(response.status_code, response.text)


def send_template_email(to_email, to_name, template_id, **variables):
    return _send_template_email(
        public_key=settings.MAILJET_PUBLIC_KEY,
        private_key=settings.MAILJET_PRIVATE_KEY,
        to_email=to_email,
        to_name=to_name,
        template_id=template_id,
        variables=variables,
    )


@shared_task
def send_verification_email_link(to_email, to_name, link, firstname):
    return send_template_email(
        to_email,
        to_name,
        template_id=settings.MAILJET_EMAIL_TEMPLATE_ID,
        link=link,
        firstname=firstname
    )
