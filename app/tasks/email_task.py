import asyncio

from app.services.email import send_verification_email
from app.services.security import generate_verification_url
from app.workers.celery import celery


@celery.task(name="email_task")
def send_email_task(data: dict):
    url = asyncio.run(generate_verification_url(data["verification_code"]))
    asyncio.run(send_verification_email(data["email"], data["username"], url))
    return url
