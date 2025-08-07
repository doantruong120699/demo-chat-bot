from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("User must have an email address.")

        # if not username:
        #     raise ValueError("User must have an username.")

        user = self.model(email=self.normalize_email(email), **kwargs)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.model(
            email=self.normalize_email(email), is_superuser=True, **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
