#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 13:56:14 2016

@author: enewton
"""

import numpy as np

def delfosse(absk):
    mm = np.power(10, 1e-3*(1.8 + 6.12*absk + 13.205*absk**2 - 6.2315*absk**3 + 0.37529*absk**4))
    return mm
