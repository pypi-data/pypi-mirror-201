#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import math
import random

from messaging_app.func.miller_rabin import is_prime



def get_prime(bit):
    while True:
        num = random.randrange(2**(bit-1), 2**(bit))#random.getrandbits(bit)
        if is_prime(num):
           return num       



def gen_keys(bit):
    p = get_prime(bit)

    q = get_prime(bit)

    n = p * q
    m = (p - 1) * (q - 1)
    e = get_e(m,bit)
    d = get_d(e, m)
    while d < 0:
        d += m
    return [p, q, n, e, d]


def get_e(m,bit):
    """Finds an e coprime with m."""
    #e = 2
    e = get_prime(bit)
    while gcd(e, m) != 1:
        e += 1
    return e


def gcd(a, b):
    """Euclid's Algorithm: Takes two integers and returns gcd."""
    while b > 0:
        a, b = b, a % b
    return a

def get_d(e, m):
    x = lasty = 0
    lastx = y = 1
    while m != 0:
        q = e // m
        e, m = m, e % m
        x, lastx = lastx - q*x, x
        y, lasty = lasty - q*y, y
    return lastx

