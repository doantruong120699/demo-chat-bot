from django.utils.translation import gettext_lazy as _

# Authentication
USERNAME_ALREADY_EXISTS = _("Username already exists!")

SIGN_UP_SUCCESSFUL = _("Signup successful.")
CONDITION_PASSWORD_VALID = _("Password invalid format.")
DONT_MATCH_CURRENT_PASSWORD_PLEASE_CHECK_AGAIN = _(
    "Dont match current password. Please check again"
)

THE_EMAIL_ADDRESS_OR_PASSWORD_IS_INCORRECT = _("Please check your email or password.")
THE_USER_HAD_BEEN_DELETED_FROM_THE_SYSTEM = _(
    "The User had been deleted from the system."
)
USER_IS_NOT_ACTIVE = _("Waiting for administrator approval.")
USER_IS_BLOCKED = _(
    "This account has been suspended..\n Please contact the administrator."
)
USER_IS_CANCEL = _("This account has been cancelled.")
USER_FORGOT_PASSWORD_SUCCESS = _("User forgot password success.")
THIS_URL_IS_INVALID = _("This URL is invalid.")
THIS_TOKEN_IS_INVALID = _("This Token is invalid.")
THIS_TOKEN_IS_EXPIRED = _("This token is expired.")
USER_IS_NOT_VERIFY_MAIL = _("User is not verify email.")
VERIFY_MAIL_SUCCESS = _("Verify mail success.")
RESEND_VERIFY_MAIL_SUCCESS = _("Please check your email address.")
RESET_PASSWORD_SUCCESS = _("Reset password success.")
CHANGE_PASSWORD_SUCCESS = _("Change password success")
# THIS_EMAIL_NOT_YET_REGISTER = _('This email not yet register')
THIS_EMAIL_VERIFIED = _("This email verified.")
THIS_EMAIL_IS_ALREADY_REGISTERED = _("This email is already registered.")
THE_AUTHENTICATION_NUMBER_DOES_NOT_MATCH = _(
    "The authentication number does not match."
)
OTP_SMS_NOT_MATCH = _("The authentication phone number does not match.")
USER_OVERSEA_MUST_BE_HAVE_COUNTRY = _("User oversea must be have country.")
THIS_EMAIL_IS_NOT_REGISTER = _("This email is not registered.")
THIS_ID_IS_NOT_REGISTER = _("This ID is not registered.")

THIS_ID_HAS_ALREADY_BEEN_REGISTERED = _("This ID has already been registered.")
CAN_NOT_REQUEST = _("Can not request to seller.")
