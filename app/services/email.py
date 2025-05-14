import asyncio
import logging
import os

import sib_api_v3_sdk
from jinja2 import Environment, FileSystemLoader
from pydantic import EmailStr
from sib_api_v3_sdk.rest import ApiException

from app.core.config import settings

SMTP_KEY = settings.SMTP_KEY
SMTP_LOGIN = settings.SMTP_LOGIN
SMTP_SERVER = settings.SMTP_SERVER
SMTP_PORT = settings.SMTP_PORT
MAIL_FROM = settings.MAIL_FROM

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))


async def render_template(template_name: str, context: dict) -> str:
    template = env.get_template(template_name)
    return template.render(context)


async def send_email(
    recipient_email: EmailStr, recipient_name: str, subject: str, html_content: str
):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = SMTP_KEY

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    sender = {"email": MAIL_FROM, "name": "Auth Service"}
    recipient = [{"email": recipient_email, "name": recipient_name}]

    email_data = sib_api_v3_sdk.SendSmtpEmail(
        to=recipient, sender=sender, subject=subject, html_content=html_content
    )

    def _send_email():
        try:
            api_instance.send_transac_email(email_data)
        except ApiException as e:
            logging.warn(f"Exception when calling API: {e}\n")

    await asyncio.to_thread(_send_email)


async def send_verification_email(
    email: EmailStr, username: str, verification_url: str
):
    subject = "Email Verification"
    html_content = await render_template(
        "email_verification.html",
        {"verification_url": verification_url, "username": username},
    )

    await send_email(email, username, subject, html_content)
