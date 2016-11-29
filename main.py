"""
CS6001 - Project 2 - Elliptic curve Diffie-Hellman (ECDHE)

See the README.md for more information

Help from: https://www.youtube.com/watch?v=F3zzNa42-tQ
"""

from curves import curves
from user import User

curve = curves['secp160r2']

# Note: More curves available from: http://www.secg.org/SEC2-Ver-1.0.pdf
# Or really just use Google, just make sure they have the curved already
#   converted to hex for easy copying into this program

print("Using {}\n".format(curve))

alice = User("Alice", curve)
print(alice)

bob = User("Bob", curve)
print(bob)

# Alice and Bob exchange their public keys and calculate the shared secret.
alice.generate_shared_secret(bob.public_key)
bob.generate_shared_secret(alice.public_key)

print("""Shared Secrets:
-> Alice: {}
-> Bob: {}
""".format(alice.shared_secret, bob.shared_secret))

print("Do Alice and Bob's shared secrets match? {}".format(
    "YES" if alice.shared_secret == bob.shared_secret else "NO"
))
