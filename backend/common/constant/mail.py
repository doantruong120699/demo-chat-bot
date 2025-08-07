from enum import Enum
from django.conf import settings


class MailFields(str, Enum):
    IS_SEND_ONLY_USER = "is_send_only_user"
    FROM_EMAIL = "from_email"
    TO = "to"
    BCC = "bcc"
    CC = "cc"
    REPLY_TO = "reply_to"
    SUBJECT = "subject"
    HTML_TEMPLATE_NAME = "html_template_name"
    TXT_TEMPLATE_NAME = "plain_template_name"
    CONTEXT = "context"


class MailTemplateEnum(Enum):
    VERIFY_EMAIL = (1, "verify_email", f"[{settings.WEBSITE_NAME}] VERIFY EMAIL")
    RESET_PASSWORD = (
        2,
        "reset_password",
        f"[{settings.WEBSITE_NAME}] RESET YOUR PASSWORD",
    )
    RESET_PASSWORD_SUCCESSFUL = (
        3,
        "reset_password_successful",
        f"[{settings.WEBSITE_NAME}] RESET PASSWORD SUCCESSFUL",
    )

    @property
    def id(self):
        return self.value[0]

    @property
    def template_html(self):
        return f"email/{self.value[1]}.html"

    @property
    def template_txt(self):
        return f"{self.value[1]}.txt"

    @property
    def subject_mail(self):
        return self.value[2]
