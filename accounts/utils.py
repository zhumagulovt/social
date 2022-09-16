from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from django.contrib.auth import get_user_model

User = get_user_model()


def send_confirmation_link(template, user, path, title):

    html_message = render_to_string(template, {
        "user": user,
        "protocol": "http",
        "domain": f"localhost:3000/{path}",
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": default_token_generator.make_token(user)
    })

    message = EmailMessage(
        title,
        html_message,
        "example@example.com",
        [user.email]
    )
    message.content_subtype = 'html'
    message.send()