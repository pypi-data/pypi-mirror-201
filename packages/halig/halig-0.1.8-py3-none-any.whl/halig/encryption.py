from pyrage import decrypt as rage_decrypt
from pyrage import encrypt as rage_encrypt
from pyrage import ssh, x25519

from halig.settings import Settings


class Encryptor:
    """Encryption utility class

    Attributes:
        settings (Settings): a Settings instance
    """

    def __init__(self, settings: Settings):
        self.settings = settings

        # load identity
        with settings.identity_path.open("r") as f:
            identity_contents = f.read()
        if identity_contents.startswith("-----BEGIN OPENSSH PRIVATE KEY-----"):
            self.identity = ssh.Identity.from_buffer(identity_contents.encode())
        else:
            self.identity = x25519.Identity.from_str(identity_contents)

        # load recipient
        with settings.recipient_path.open("r") as f:
            recipient_contents = f.read()
        if recipient_contents.startswith("ssh-ed25519"):
            self.recipient = ssh.Recipient.from_str(recipient_contents)
        else:
            self.recipient = x25519.Recipient.from_str(recipient_contents)

    def encrypt(self, data: str | bytes) -> bytes:
        if isinstance(data, str):
            data = data.encode()
        return rage_encrypt(data, [self.recipient])  # type: ignore[no-any-return]

    def decrypt(self, data: bytes) -> bytes:
        return rage_decrypt(data, [self.identity])  # type: ignore[no-any-return]
