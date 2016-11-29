from user import User


def run(curve):
    """Runs the "simple" version of the ECDHE
    """
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
