from django.core import mail
from django.core.mail import send_mail
from django.dispatch import receiver
from django.template.loader import render_to_string
from django_rest_passwordreset.signals import reset_password_token_created

from ashar_app.settings import DOMAIN,  RESET_PASSWORD_DOMAIN
from django.utils.html import strip_tags
from ashar_app.settings import REDIRECT_DOMEN


def send_confirmation_email(user):
    # token = jwt.encode({"user": email}, SECRET_KEY, algorithm="HS256").decode("utf-8")
    context = {
        "small_text_detail": "Thank you for "
        "creating an account. "
        "Please verify your email "
        "address to set up your account.",
        "email": user.email,
        "domain": DOMAIN,
        'activation_code': user.activation_code
    }
    msg_html = render_to_string("account/email.html", context)
    plain_message = strip_tags(msg_html)
    subject = "Account activation"
    # from_email = ("alymbekovdastan1@gmail.com",)
    to_emails = user.email
    mail.send_mail(
        subject,
        plain_message,
        "alymbekovdastan1@gmail.com",
        [to_emails, ],
        html_message=msg_html,
    )


def send_activation_mail(user):
    subject = f'Активация аккаунта на сайте маркетплейс'
    body = f'Благодарим Вас за регистрацию на нашем сайте'\
           f'Для активации аккаунта пройдите по ссылке:'\
           f'{REDIRECT_DOMEN}/v1/accounts/activate/{user.activation_code}/'
    from_email = 'alymbekovdastan1@gmail.com'
    recipients = [user.email]
    mail.send_mail(subject=subject, message=body, from_email=from_email, recipient_list=recipients, fail_silently=False)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    context = {
        "small_text_detail": "Your password reset successfully",
        "for_pass_confirm": "Press this button for create new password",
        "info_for_create": "Copy this token and put in 'Password confirm' link, then enter new password",
        "email": reset_password_token.user.email,
        "domain": RESET_PASSWORD_DOMAIN,
        "token": reset_password_token.key
    }

    msg_html = render_to_string("account/reset_password_email.html", context)
    plain_message = strip_tags(msg_html)
    subject = "Reset password"

    send_mail(
        subject,
        plain_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email],
        html_message=msg_html,
    )
