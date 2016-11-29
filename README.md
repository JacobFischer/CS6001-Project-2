# CS6001-Project-2

Project 2 for the MST FS2016 CS6001 - Cryptography course, implementing Elliptic curve Diffie–Hellman (ECDHE)

## Requirements

[Python 3][python] is the only requirement. This works on the MST campus CS building machines just fine.

## How to Run

```
python3 main.py
```

That should use the default curve (secp160r2) and have Alice and Bob generate keys and see if they can generate a shared secret.

### Networked Example

Using simple TCP Sockets we also can demonstrate how to securely verify generate the shared secret without disclosing the private keys. To do just run a different script in two terminals:

#### First Terminal
```
python3 main.py --server
```

#### Second Terminal
```
python3 main.py --client
```

They will connect to each other and do the key exchanges via networked communications instead of in memory in the toy example contained in `main.py`.

### Curve Overrides

If you wish to control the values of the curve by choosing a different defined curve in the `curves.py` file via the CLI `--curve NAME`. Alternatively you can override specific curve properties via their name, e.g. `--a 0 --b 7`. Though be warned, if you define a custom curve and it is not a proper elliptical curve the ECDHE will probably fail and throw an exception complaining something is wrong (e.g. a point cannot be found on the given curve because it is invalid).

## Using different curves

See http://www.secg.org/SEC2-Ver-1.0.pdf and take the parameters from there. I used secp160r2 from page 11.

## Documentation

Everything is fully documented using docstrings. Care has been taken to adhere to [Google][google] and [PEP8][pep8]'s style guidelines.

[python]: https://www.python.org/
[google]: https://google.github.io/styleguide/pyguide.html
[pep8]: https://www.python.org/dev/peps/pep-0008/
