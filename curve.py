from point import Point, inf

class EllipticCurve:
    """Represents an elliptic curve for ECDHE when given parameters for the curve
    """

    def __init__(self, p, a, b, g, n, h, name="Unnamed"):
        # the field characteristic
        self.p = p

        # the curve coefficients
        self.a = a
        self.b = b

        # the base point on this curve
        self.g = g

        # the subgroup order
        self.n = n

        # the subgroup cofactor
        self.h = h

        # helpful variables for future references
        self.name = name

        # to represent the infinity point on this line
        self.infinity_point = Point(inf, inf, self)

        # g as a Point instance, needed for private key generation
        self.point = Point(self.g[0], self.g[1], self)

    def contains(self, point):
        """Checks if a point is on this curve

        Args:
            point: the point to check against

        Returns:
            bool: True if this curve contains the given point, false otherwise
        """

        if not point:
            raise Exception("Point is nothing")

        # special case: check if point at infinity
        if point.is_infinity():
            # then the point is at infinity, which is on the curve
            return True

        # else see if the p is on the curve via: y^2 - x^3 - a*x - b % p == 0
        # Note: Math.pow didn't work here, weird
        y2 = point.y * point.y
        x3 = point.x * point.x * point.x
        return (y2 - x3 - self.a * point.x - self.b) % self.p == 0

    def __str__(self):
        """
        str override

        Returns:
            str: Human readable string format of this curve

        TODO:
            Maybe parse the field characteristic to make the actual equation, e.g.
            p = FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFE FFFFAC73
            p = 2^160-2^32-2^14-2^12-2^9-2^8-2^7-2^3-2^2-1
        """
        return "{} Curve".format(self.name)
