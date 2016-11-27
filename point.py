# Note: math.inf doesn't seem to work, but this does :P
inf = float("inf")

class Point:
    """Represents a point on an elliptical curve
    """

    def __init__(self, x, y, curve):
        """Initializes a point at a given (x, y)

        Args:
            x: a number for the x-coordinate of the point
            y: a number for the y-coordinate of the point
            curve: the elliptical curve that this point lies on

        Raises:
            Exception: If the given (x, y) do not lie on the given curve
                an exception will be raised
        """

        self.x = x
        self.y = y

        if not self.is_infinity():
            # make sure (x, y) is within the curve before checking
            self.x = self.x % curve.p
            self.y = self.y % curve.p

        if not curve.contains(self):
            raise Exception("Point {} is not on curve {}".format(self, curve))

        self.curve = curve

    def is_infinity(self):
        """Checks if this point is the point that lies at infinity

        Returns:
            bool: True if this point lies at infinity, False otherwise
        """
        return self.x == inf and self.y == inf

    def __neg__(self):
        """Creates the -self version of this point

        Returns:
            Point: -self, this point inverted along the y axis
        """
        if self.is_infinity():
            return self # no need to negate

        p = Point(
            x = self.x,
            y = -self.y % self.curve.p,
            curve = self.curve
        )

        return p

    def __eq__(self, point):
        """== equality override, to check if two different Point instances
            are on the same (x, y)

        Args:
            point: the other point to compare our (x, y) to

        Returns:
            bool: True if the two points are on the same (x, y), False otherwise
        """
        return self.x == point.x and self.y == point.y

    def __str__(self):
        """str override

        Returns:
            str: human readable string, literally (x, y)
        """
        return "({}, {})".format(self.x, self.y)
