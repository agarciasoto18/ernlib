import lfa
import math
import numpy

## Solar U,V,W relative to LSR from Dehnen & Binney 1998.
##sol_uvw = numpy.array([ 10.00, 5.25, 7.17 ])
#lsr_vel = numpy.array([11, 12, 7])
#
## Rough peculiar velocity outer boundaries for thin and thick disc.
## Still trying to find a reference.
#vpec_thin  =  85  # km/s
#vpec_thick = 180  # km/s

def radec2uvw(ara, ade,         # rad
              apmra, ae_pmra,   # arcsec/yr
              apmde, ae_pmde,   # arcsec/yr
              aplx,  ae_plx,    # arcsec
              avrad, ae_vrad):  # km/s

  # Method of Johnson & Soderblom (1987) but in ICRS.

  uvw = numpy.zeros((len(ara),3))
  e_uvw = numpy.zeros((len(ara),3))

  for i,(ra,de,pmra,e_pmra,pmde,e_pmde,plx,e_plx,vrad,e_vrad) in \
      enumerate(zip(ara,ade,apmra,ae_pmra,apmde,ae_pmde,aplx,ae_plx,avrad,ae_vrad)):

      kop = lfa.AU / (lfa.JYR*lfa.DAY*1000*plx)

      sa = math.sin(ra)
      ca = math.cos(ra)
      sd = math.sin(de)
      cd = math.cos(de)
    
      T = lfa.eq2gal
      A = numpy.array([[ ca*cd, -sa, -ca*sd ],
                       [ sa*cd,  ca, -sa*sd ],
                       [    sd,   0,     cd ]])
    
      B = numpy.dot(T, A)
      C = B*B
    
      p = numpy.array([ vrad,
                        kop*pmra,
                        kop*pmde ])
    
      v_vrad = e_vrad*e_vrad
      v_pmra = e_pmra*e_pmra
      v_pmde = e_pmde*e_pmde
    
      rv_plx = e_plx*e_plx / (plx*plx)
    
      q = numpy.array([ v_vrad,
                        kop*kop*(v_pmra + pmra*pmra*rv_plx),
                        kop*kop*(v_pmde + pmde*pmde*rv_plx) ])
    
      uvw[i] = numpy.dot(B, p)
      e_uvw[i] = numpy.sqrt(numpy.dot(C, q) +
                         2*pmra*pmde*kop*kop*rv_plx*(B[:,1]*B[:,2]).T)
  
  return uvw, e_uvw


