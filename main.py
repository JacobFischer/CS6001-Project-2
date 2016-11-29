"""
CS6001 - Project 2 - Elliptic curve Diffie-Hellman (ECDHE)

See the README.md for more information
Basically this main file parses CLI arguments to determine how to run this
program, either in simple.py or networked.py

Help from: https://www.youtube.com/watch?v=F3zzNa42-tQ
"""
from curve import EllipticCurve
import argparse
import networked
import simple

# the default curve name as defined in curves.py
default_curve_name = 'secp160r2'

# here we set up the CLI args,
# basically set if networked or simple mode, and change curve parameters
parser = argparse.ArgumentParser(description='Runs the ECDHE program')
parser.add_argument('--client', action='store_true',
                    help='If this should run as a networked client')

parser.add_argument('--server', action='store_true',
                    help='If this should run as a networked server')

parser.add_argument('--port', type=int, default=5555,
                    help='The port to connect through as a client/server')

parser.add_argument('--host', default='localhost',
                    help='The host to connect to as a client')

# curves
parser.add_argument('--curve', default=default_curve_name,
                    help='The name of the curve to use')
parser.add_argument('--p', type=int,
                    help='The field characteristic of the curve')
parser.add_argument('--a', type=int,
                    help='The field coefficient `a` of the curve')
parser.add_argument('--b', type=int,
                    help='The field coefficient `b` of the curve',)
parser.add_argument('--gx', type=int,
                    help='The g_x base point on the curve')
parser.add_argument('--gy', type=int,
                    help='The g_y base point on the curve')
parser.add_argument('--n', type=int,
                    help='The subgroup order on the curve')
parser.add_argument('--h', type=int,
                    help='The subgroup cofactor on the curve')

args = parser.parse_args()

# if they defined a custom curve this is its value(s)
curve = EllipticCurve(
    name=args.curve,
    p=args.p,
    a=args.a,
    b=args.b,
    gx=args.gx,
    gy=args.gy,
    n=args.n,
    h=args.h
)

# figure out which file to run
if not args.client and not args.server:
    # then just run the "simple.py" non networked example
    simple.run(curve)
else:
    # then run the "networked.py" example

    # if they are a client send the host, otherwise None to act as server
    host = args.host if args.client else None
    networked.run(curve, args.port, host)
