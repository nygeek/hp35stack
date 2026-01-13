# HP35Stack

## About

The HP35 calculator had four primary registers arranged in a stack.
The four registers were called X, Y, Z, and T.  In addition there
was a memory register called M.  Our implementation of the HP35
stack defaults to eight elements rather than four.  The bottom four
are shown as X, Y, Z, and T, but the rest are simply shown by their
index.

## As used in CNC (Complex Number Calculator)

On the HP35 calculator the bottom register, called X, was always
displayed.  For CNC, we display the entire stack and the M register
every time the enter key is pressed.

On the HP35, pressing enter would push the number in X up to Y, Y
up to Z, and Z up to T.  When this was done the value in T was lost.

Roll down, shown on the HP35 keyboard with the letter R and a down
arrow, would move T to Z, Z to Y, Y to X, and X around to T.  We
call this 'down'.

STO would take the value in X and save it in M.  RCL would replace
the value in X with the value stored in M.

A unary function would replace the value of X with the result of
the function.

A binary function would operate on X and Y.  The result would be
left in X and the values above in the stack would be pulled down:
Z to Y, T to Z.  The value in T would remain, so after any binary
operation the T and Z registers would hold the same value.

## Installation

This module should be installed to support the CNC.  Since none of this has
been added to a public Python library, you will need to install it locally
on your machine.  For the purposes of discussion, let's assume that it is
installed at ```~/projects/h/hp35stack/```

```> git clone https://github.com/nygeek/hp35stack.git```

And then install it for the calculator that uses the stack:

```> pip install -e ~/projects/h/hp35stack```

## Known bugs

At this point there are two modules: hp35stack.py (cmath complex
type) and hp35stack10.py (CMath10 type).  There should be only one.
When the Round TUIT arrives I will rebuild these as a single class
that is parameterized with the class that it manipulates.

## License

Apache License 2.0

## Authors

Marc Donner (marc.donner@gmail.com)
