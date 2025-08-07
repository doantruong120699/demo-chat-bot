from cryptography.fernet import Fernet, MultiFernet
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import cached_property


class FieldCrypter:
    """Encryption Utils."""

    def __init__(self, key):
        super(FieldCrypter, self).__init__()
        self.key = key

    @cached_property
    def keys(self):
        """Get keys for encryption and decryption."""
        key = self.key
        if key is None:
            raise ImproperlyConfigured("Cryptographic key is not properly configured")
        return [Fernet(key=key)]

    @cached_property
    def crypter(self):
        """Get the crypter for encryption and decryption process."""
        return MultiFernet(self.keys)

    @staticmethod
    def generate_key():
        """Generate cryptographic key."""
        return Fernet.generate_key()

    def encrypt(self, text) -> str:
        """Do text encryption.
        Args:
            text (str): input text for encryption
        Returns
            encrypted text (str)
        """
        return self.crypter.encrypt(text.encode("utf-8")).decode("utf-8")

    def decrypt(self, text) -> str:
        """Do text decryption.
        Args:
            text (str):
        """
        return self.crypter.decrypt(text.encode("utf-8")).decode("utf-8")
