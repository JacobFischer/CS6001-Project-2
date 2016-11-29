from point import Point, inf
import curves


class EllipticCurve:
    """Represents an elliptic curve for ECDHE when given parameters for the curve
    """

    def __init__(self, **kwargs):
        """Initializes an Elliptic curve

        Args:
            name: the name of the curve as defined in curves,
                or property overrides for p, a, b, g, n, or h
        """

        properties = dict(**kwargs)
        # see if the curve is known
        standard_properties = curves.get(properties['name'])

        # check each curve property for an override
        for key in ('p', 'a', 'b', 'gx', 'gy', 'n', 'h'):
            if key not in properties or not properties[key]:
                if standard_properties:
                    properties[key] = standard_properties[key]
                else:
                    raise Exception(
                        "Custom curve missing property {}".format(key)
                    )

        # the field characteristic
        self.p = properties['p']

        # the curve coefficients
        self.a = properties['a']
        self.b = properties['b']

        # the base point on this curve
        self.g = (properties['gx'], properties['gy'])

        # the subgroup order
        self.n = properties['n']

        # the subgroup cofactor
        self.h = properties['h']

        # helpful variables for future references
        self.name = properties['name']

        # store this in-case we need to send the values to a client
        self.base_properties = properties

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
            Maybe parse the field characteristic to make the actual equation,
            e.g.
                p = FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFE FFFFAC73
                p = 2^160-2^32-2^14-2^12-2^9-2^8-2^7-2^3-2^2-1
        """
        return "{} Curve".format(self.name)
