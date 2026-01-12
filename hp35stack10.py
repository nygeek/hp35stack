""" Implementation of the hp35 stack for the CNC10 calculator

    The original hp35stack class works on complex numbers.  This
    one will work with the long numbers from the decimal library
    and ultimately on complex numbers constructed from long decimals.

Adapted from the original hp35stack.py starting 2025-12-19

Copyright (C) 2025 Marc Donner

$Id: hp35stack10.py,v 1.3 2025/12/19 19:20:38 marc Exp $

ToDo:

"""

# --------- Python Libraries --------- #

import json
# import cmath
from decimal import Decimal

# ---------- JSON Encoder for Decimal ---------- #

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)

def decimal_decoder(dct):
    for key, value in dct.items():
        if isinstance(value, str):
            try:
                dct[key] = Decimal(value)
            except:
                pass
    return dct

# --------- HP 35 Stack Class --------- #

class HP35Stack10:
    """ Class to implement the HP35 Stack and sto/rcl register """

    def __init__(self, depth=4, rel_tol=1e-10 ):
        _zero = Decimal("0")
        self.stack = [_zero] * depth
        self.depth = depth
        self.rel_tol = rel_tol
        self.labels = ['0'] * depth
        for j in range(4, depth):
            self.labels[j] = str(j)
        self.labels[0] = "X"
        self.labels[1] = "Y"
        self.labels[2] = "Z"
        self.labels[3] = "T"
        self.storcl = _zero
        self.count = 0


    def __str__(self):
        _result = "M: " + str(self.storcl) + "\n\n"
        for j in range(self.depth - 1, -1, -1):
            _result += self.labels[j] + ": " + str(self.stack[j]) + "\n"
        return _result


    def push(self, cn):
        """ push a number on to the stack """
        # this destroys the value at the top of the stack
        for j in range(self.depth - 1, 0, -1):
            self.stack[j] = self.stack[j-1]
        # With the switch to decimal, we will omit use of clamp
        # _result = self.clamp(cn)
        # self.set_x(_result)
        # return _result
        self.set_x(cn)
        return cn



#   def clamp(self, z):
#       """ clamp real and imag parts of z to within clamp of ints """
#       _r = complex(z).real
#       _i = complex(z).imag
#       if self.rel_tol != 0:
#           if round(abs(z)) != 0:
#               if cmath.isclose(_r, round(_r),
#                                rel_tol=self.rel_tol,
#                                abs_tol=self.rel_tol):
#                   _r = round(_r)
#               if cmath.isclose(_i, round(_i),
#                                rel_tol=self.rel_tol,
#                                abs_tol=self.rel_tol):
#                   _i = round(_i)
#       return complex(_r, _i)


    def pop(self):
        """ pop the bottom element (x) from the stack and return it """
        # this rolls the stack down, thus replicating t into z
        _result = self.stack[0]
        for j in range(0, self.depth - 1):
            self.stack[j] = self.stack[j+1]
        return _result


    def rolldown(self):
        """ perform the roll down function """
        _t = self.stack[0]
        for j in range(0, self.depth - 1):
            self.stack[j] = self.stack[j+1]
        self.stack[self.depth - 1] = _t


    def get_count(self):
        """ return the count """
        return self.count


    def increment_count(self):
        """ increment the count of stack interactions """
        self.count += 1
        return self.count


    def set_x(self, new_x):
        """ retrieve the x value from the stack """
        self.stack[0] = new_x
        return self.stack[0]


    def sto(self):
        """ sto function - copy x to M """
        self.storcl = self.stack[0]
        return self.stack[0]


    def rcl(self):
        """ rcl function - copy M to x (push the rest up) """
        self.push(self.storcl)


    def exch(self):
        """ exchange the values of x and y """
        x = self.stack[0]
        self.stack[0] = self.stack[1]
        self.stack[1] = x

    def clear(self):
        """ clear the stack """
        _zero = Decimal('0')
        self.stack = [_zero] * self.depth
        self.storcl = _zero


    def stack_to_json(self):
        """ a json representation of the stack """
        stack = [[0, 0]] * self.depth
        result = {}
        for i in range(0, self.depth):
            stack[i] = [self.stack[i].real, self.stack[i].imag]
        result['stack'] = stack
        result['storcl'] = [self.storcl.real, self.storcl.imag]
        result['rel_tol'] = self.rel_tol
        result['depth'] = self.depth
        result['count'] = self.count
        return json.dumps(result, cls=DecimalEncoder)


    def load_stack_from_json(self, stack_as_json):
        """ given a json string, reconstitute the stack """
        new = json.loads(stack_as_json, object_hook=decimal_decoder)
        if 'depth' in new:
            self.depth = new['depth']
        if 'rel_tol' in new:
            self.rel_tol = new['rel_tol']
        if 'count' in new:
            self.count = new['count']
        if 'stack' in new:
            for j in range(0, self.depth):
                self.stack[j] = Decimal(new['stack'][j][0])
        if 'storcl' in new:
            self.storcl = Decimal(new['storcl'][0])


def main():
    """ Simple unit tests. """
    stack = HP35Stack10(8)
    print(f"Stack:\n{stack}")
    _three = Decimal('3')
    stack.push(_three)
    _two = Decimal('2')
    stack.push(_two)
    _one = Decimal('1')
    stack.push(_one)
    _zero = Decimal('-1')
    stack.push(_zero)
    print(f"Stack:\n{stack}")
    qq = stack.stack[0]
    print(f"x: {qq}")
    qq = stack.pop()
    print(f"pop =>: {qq}")
    print(f"Stack:\n{stack}")
    stack.push(_two)
    stack.push(_one)
    stack.sto()
    stack.exch()
    stack.rcl()
    json_stash = stack.stack_to_json()
    print(f"json_stash: {json_stash}")
    # now let's clear the stack
    stack.clear()
    print(f"Stack:\n{stack}")
    # now reconstitute the stack ...
    stack.load_stack_from_json(json_stash)
    print(f"Stack:\n{stack}")


if __name__ == '__main__':
    main()
