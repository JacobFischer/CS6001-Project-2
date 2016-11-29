from connection import Connection
from curve import EllipticCurve
from user import User


def run(curve, port, host):
    """runs the networked example as a client or server

    Args:
        curve: The elliptical curve to use, clients ignore this
        port: The port to connect through
        host: The host to connect through if a client, servers ignore this
    """
    is_server = not host
    user = None

    # 1. Connect:
    #   If we are the server we create a port listening for the other user
    #   If we are the client we attempt to connect to the other user listening
    #       for us

    connection = Connection(port, host)

    # 2. Create the Curve

    if is_server:
        # first we need to tell the other user what curve we are using
        connection.send(curve.base_properties)
    else:
        # first we need to wait for the curve being sent above
        curve_properties = connection.read()
        curve = EllipticCurve(**curve_properties)
    connection.curve = curve
    print("Using {}\n".format(curve))

    # 3. Create our users
    user = User("Alice" if is_server else "Bob", curve)
    print(user)

    # 4. Exchange public keys
    connection.send(user.public_key)
    their_public_key = connection.read()
    print("Other user's public key:\n-> {}\n".format(their_public_key))

    # 5. Create the shared secret
    user.generate_shared_secret(their_public_key)
    connection.send(user.shared_secret)

    # 6. See if our shared secret matches theirs
    their_shared_secret = connection.read()

    print("""Shared Secrets:
    -> Us: {}
    -> Them: {}
    """.format(user.shared_secret, their_shared_secret))

    print("Do Alice and Bob's shared secrets match? {}".format(
        "YES" if user.shared_secret == their_shared_secret else "NO"
    ))

    # 7. Done!
    # After this point the shared_secrets should match, so we can use to
    #   encode/decode messages back and forth.
    # Obviously there are some issues with doing that straight up, and the next
    #   obvious solution would be to use a digital signature algorithm like ECDSA.
    # However, for now we've demonstrated how to verify secrets without disclosing
    #   each users' private keys, so let's close the connection and exit the script

    connection.close()
