import logging
from email import encoders
from email.mime.base import MIMEBase

from django.conf import settings
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.utils.translation import gettext_lazy as _
from common.constant.mail import MailTemplateEnum

logger = logging.getLogger(__name__)


class MailService:

    def __init__(self):
        super(MailService, self).__init__()

    def send_email_template_by_type(
        self,
        email_type_enum: MailTemplateEnum,
        recipient_mails=[],
        context={},
        **kwargs,
    ):
        self.__send_email_template(
            subject=email_type_enum.subject_mail,
            recipient_mails=recipient_mails,
            html_template_path=email_type_enum.template_html,
            context=context,
            fail_silently=False,
            **kwargs,
        )

    def __send_email_template(
        self,
        subject,
        recipient_mails,
        plain_template_path=None,
        html_template_path=None,
        context=None,
        attachments=None,
        **kwargs,
    ):
        try:
            if not plain_template_path and not html_template_path:
                raise ValueError(
                    _(
                        "Send mail with template must not empty plain or html template path"
                    )
                )
            if plain_template_path:
                plain_template = get_template(plain_template_path)
                message = plain_template.render(context=context)
            else:
                message = ""

            if html_template_path:
                html_template = get_template(html_template_path)
                html_message = html_template.render(context=context)
            else:
                html_message = ""

            if attachments:
                msg = EmailMultiAlternatives(
                    subject=subject,
                    body=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=recipient_mails,
                    **kwargs,
                )
                msg.attach_alternative(html_message, "text/html")

                for attachment in attachments:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f'attachment; filename="{attachment.name}"',
                    )
                    msg.attach(part)

                msg.send()
            else:
                mail.send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=recipient_mails,
                    html_message=html_message,
                    **kwargs,
                )
        except Exception as ex:
            logger.exception("Send mail fail: ", ex)
            raise ex
