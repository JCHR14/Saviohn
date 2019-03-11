from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
	def _make_hash_value(self, user, timestamp):
		return (
			six.text_type(user.pk) + six.text_type(timestamp) +
			six.text_type(user.profile.auth_email_confirmed)
		)

account_activation_token = AccountActivationTokenGenerator()


class AccountResetTokenGenerator(PasswordResetTokenGenerator):
	def _make_hash_value(self, user, timestamp):
		return (
			six.text_type(user.pk) + six.text_type(timestamp) +
			six.text_type(user.profile.auth_email_confirmed)
		)

account_reset_token = AccountResetTokenGenerator()