"""
CS6001 - Project 2 - Elliptic curve Diffie-Hellman (ECDHE)

See the README.md for more information

Help from: https://www.youtube.com/watch?v=F3zzNa42-tQ

"""

from curve import EllipticCurve
from user import User

curve = EllipticCurve(
    name = 'secp160r2', # see http://www.secg.org/SEC2-Ver-1.0.pdf, pg 11
    # The field characteristic
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFAC73,
    # The curve coefficients, could be taken in as user input
    a = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFAC70,
    b = 0xB4E134D3FB59EB8BAB57274904664D5AF50388BA,
    # The base point on this curve
    g = (
        0x52DCB034293A117E1F4FF11B30F7199D3144CE6D,
        0xFEAFFEF2E331F296E071FA0DF9982CFEA7D43F2E
    ),
    # The subgroup order
    n = 0x00000000000000000000351EE786A818F3A1A16B,
    # The subgroup cofactor
    h = 1
)

# Note: More curves available from: http://www.secg.org/SEC2-Ver-1.0.pdf
# Or really just use Google, just make sure they have the curved already
#   converted to hex for easy copying into this program

print("Using {}\n".format(curve))

alice = User("Alice", curve)
print(alice)

bob = User("Bob", curve)
print(bob)

# Alice and Bob exchange their public keys and calculate the shared secret.
# TODO: network this for extra credit
alice.generate_shared_secret(bob.public_key)
bob.generate_shared_secret(alice.public_key)

print("""Shared Secrets:
-> Alice: {}
-> Bob: {}
""".format(alice.shared_secret, bob.shared_secret))

print("Do Alice and Bob's shared secrets match? {}".format(
    "YES" if alice.shared_secret == bob.shared_secret else "NO"
))
