from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # PK, 현재시간, 활성화 정보를 토대로 token을 생성한다.
        return (six.text_type(user.pk) + six.text_type(timestamp)) +  six.text_type(user.is_active)

account_activation_token = AccountActivationTokenGenerator()