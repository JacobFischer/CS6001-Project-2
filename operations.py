import math
from point import Point

# note: Math.pow seems to give out incorrect
#   return values with numbers these large :P


def group_add(p, q):
    """Group Addition: adds two points p and q returning a new point r

        Args:
            p: the first point
            q: the second point

        Returns:
            Point: an r such that r = p + q on the EllipticeCurve they share

        Raises:
            Exception: If the two points being added are not on the save curve
    """

    # check to make sure both points are on this curve
    if p.curve != q.curve:
        raise Exception(
            "{} and {} are not on the same curves {} and {}"
            .format(p, q, p.curve, q.curve)
        )

    if p.is_infinity():
        # inf + q = q
        return q

    if q.is_infinity():
        # p + int = p
        return p

    # if they are the same vertical coordinate
    if p.x == q.x:
        # and if they also are on the same horizontal coordinate
        if p.y == q.y:
            # then they are the same points
            slope = (3*p.x*p.x+p.curve.a) * modular_inverse(p.y*2, p.curve.p)
        else:
            # p + -q = inf
            # This is because we are adding vertical points
            #   hence the same x values
            return p.curve.infinity_point
    else:
        # then p != q (completely different points on the same curve)
        slope = (p.y - q.y) * modular_inverse(p.x - q.x, p.curve.p)

    # calculate the new point's x and y
    x = slope*slope - (p.x + q.x)
    y = -(slope * (p.x - x) - p.y)

    return Point(x, y, p.curve)


def scalar_multiplication(p, k):
    """Calculates q = p * k, using repeated addition

    See:
        https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication

    Args:
        p: the point to scale k times
        k: how many times to scale the point p

    Returns:
        Point: a new point q = p * k
    """

    q = p.curve.infinity_point

    if k % p.curve.n == 0 or p.is_infinity():
        # scaling inf is inf, so just return it right away
        return q

    if k < 0:
        # invert, so:
        # k * p = -k * (-p)
        return scalar_multiplication(-p, -k)

    # q = p + p + ... + p, k times (done via recursion)
    # From: https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication
    if k == 0:
        return 0  # computation complete
    elif k == 1:
        return p
    elif k % 2 == 1:
        # addition when k is odd
        return group_add(p, scalar_multiplication(p, k-1))
    else:
        # doubling when k is even
        return scalar_multiplication(group_add(p, p), k//2)


def modular_inverse(k, p):
    """Calculates the inverse of k modulo p.

    Args:
        k: a number such that k != 0
        p: a prime number

    Returns:
        a number x such that (x * k) % p == 1
    """

    if k < 0:
        # k is a negative number, so flip it
        return p - modular_inverse(-k, p)

    # find the gcd and x using the extended euclidean algorithm
    gcd, x = xgcd(k, p)

    if gcd != 1:
        raise Exception("gcd of {} and {} is {}, not 1.".format(p, k, gcd))

    if (x * k) % p != 1:
        raise Exception("calculated x is not the inverse modulus of p and k")

    return x % p  # just for safety


def xgcd(b, n):
    """ The Extended Euclidean algorithm

    See:
        https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm

    Args:
        b: a number
        n: another number

    Returns:
        number: a number g such that g = gcd(b, n)
    """
    x0, x1, y0, y1 = 1, 0, 0, 1
    while n != 0:
        q, b, n = b // n, n, b % n
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return b, x0
