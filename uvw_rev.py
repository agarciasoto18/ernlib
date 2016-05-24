# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 09:14:44 2015

@author: enewton
"""

import lfa
import math
import numpy
from numpy.linalg import inv

# this assumes NOT in LSR
# and u is the same as u in switched gal_uvw -- same sign to JI!!!

def uvw2radec(ra, de, u, v, w, plx):

  # Method of Johnson & Soderblom (1987) but in ICRS.

  pmra = numpy.zeros(len(ra))
  pmde = numpy.zeros(len(ra))
  vrad = numpy.zeros(len(ra))
  
  for i,(rr,dd,uu,vv,ww,pp) in enumerate(zip(ra,de,u,v,w,plx)):

      kop = lfa.AU / (lfa.JYR*lfa.DAY*1000*pp)
      sa = numpy.sin(rr)
      ca = numpy.cos(rr)
      sd = numpy.sin(dd)
      cd = numpy.cos(dd)

      T = lfa.eq2gal
      A = numpy.array([[ ca*cd, -sa, -ca*sd ],
                       [ sa*cd,  ca, -sa*sd ],
                       [    sd,   0,     cd ]])
    
      B = numpy.dot(T, A)
  
      z = numpy.array([uu,
                       vv,
                       ww])
      p = numpy.dot(inv(B),z)

      vrad[i] = p[0]
      pmra[i] = p[1]/kop
      pmde[i] = p[2]/kop

  
  return pmra, pmde, vrad


