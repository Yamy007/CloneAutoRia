import os

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from core.service.jwt_service import ActivateToken, JWTService


class EmailService:
    @staticmethod
    def __send_email(to: str, template_name: str, context: dict, subject=""):
        template = get_template(template_name)
        render = template.render(context)
        msg = EmailMultiAlternatives(
            subject, from_email=os.environ.get("EMAIL_HOST_USER"), to=[to]
        )
        msg.attach_alternative(render, "text/html")
        msg.send()

    @classmethod
    def register_email(cls, user):
        token = JWTService.create_token(user, ActivateToken)
        url = f"http://localhost:3000/activate/{token}"
        cls.__send_email(
            user.email, "register.html", {"name": user.email, "url": url}, "Register"
        )

    @classmethod
    def validate_email(cls, user, id):
        print("id", id)
        url = f"http://localhost:3000/validate/{id}"
        cls.__send_email(
            os.environ.get("EMAIL_ADMIN"),
            "validate.html",
            {"name": user.email, "url": url},
            "Validate",
        )
