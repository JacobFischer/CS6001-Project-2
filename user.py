import random
from operations import scalar_multiplication


class User:
    """Creates a user on a curve, basically a private/public key container
    """

    def __init__(self, name, curve):
        """Initialized a user

        Args:
            name: a string name (just for human readability)
            curve: the EllipticCurve that this user will use for private/public
                key generation
        """
        self.name = name
        self.curve = curve

        self._private_key = random.randrange(1, self.curve.n)
        self.public_key = scalar_multiplication(
            self.curve.point,
            self._private_key
        )

    def generate_shared_secret(self, other_users_public_key):
        """Generates a shared secret given another user's public key.
        If they both generate the same shared secret from each other's
        public keys then ECDHE worked

        Args:
            other_users_public_key: another User's public key
        """
        self.shared_secret = scalar_multiplication(
            other_users_public_key,
            self._private_key
        )

    def __str__(self):
        """str override

        Returns:
            str: a human readable string representation of this user and
                their keys
        """
        return ("""{self.name}:
-> Public Key {self.public_key}
-> Private Key {self._private_key}
""".format(self=self)
        )
