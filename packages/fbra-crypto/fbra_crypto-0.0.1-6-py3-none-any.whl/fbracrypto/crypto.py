import os
import signal

from cryptography.fernet import Fernet


class Crypto:
    CRYPT_IDENTIFIER = "fbra84"
    ENVIRONMENT_VAR = "FERNET_TOKEN"

    def __init__(self, environment_var="", fernet_token=""):
        if environment_var:
            self.env_var = environment_var
        else:
            self.env_var = self.ENVIRONMENT_VAR
        if fernet_token:
            fernet_token = fernet_token
        else:
            fernet_token = self.get_environment_var()
        self.encrypter = Fernet(fernet_token.encode())

    def get_environment_var(self):
        try:
            fernet_token = os.environ[self.env_var]
        except KeyError:
            fernet_token = self.get_new_fernet_token().decode()
            print(f"The environment variable '{self.env_var}' wasn't found. "
                  f"Possible new environment value '{fernet_token}' for the "
                  f"environment variable '{self.env_var}'.")
            os.kill(os.getpid(), signal.SIGTERM)
        return fernet_token

    @staticmethod
    def get_new_fernet_token():
        token = Fernet.generate_key()
        return token

    def is_ciphered(self, value):
        try:
            check = value.startswith(self.CRYPT_IDENTIFIER)
        except AttributeError:
            return False
        return check

    def cipher(self, value):
        if value == "":
            raise ValueError("Cannot chipher an empty value.")
        if not isinstance(value, str):
            value = str(value)
        data = self.encrypter.encrypt(value.encode())
        fbra_data = self.CRYPT_IDENTIFIER + data.decode()
        return fbra_data

    def decipher(self, value):
        value = value.replace(self.CRYPT_IDENTIFIER, '')
        byte_key = self.encrypter.decrypt(value.encode())
        key = byte_key.decode()
        return key

    def get_plain_value(self, value):
        if self.is_ciphered(value):
            value = self.decipher(value)
        return value
