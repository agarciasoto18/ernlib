# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 16:06:19 2016

@author: enewton
"""
import numpy as np
from scipy.integrate import trapz   

# ew = simple_fracsum(wave, flux/pseudo-1., c1, c2, mean=mean)
 
# sum up over a region, with fractions of a pixel
def fracsum(wavea, waveb, flux, c1, c2, mean=False, check=False):
  
    pixwidth = waveb-wavea  
    fracused = np.zeros_like(flux)
  
    # make sure wide enough
    if (wavea[0]>=c1) or (waveb[-1]<=c2):
      return None
    
    # whole pixels
    wholeind, = np.where( (wavea>=c1) & (waveb<=c2) )
    if len(wholeind) == 0:
      print "WARNING fracsum: no whole pixels"
    fracused[wholeind] = 1.
    
    # partial pixels
    lowind, = np.where( (wavea<c1) & (waveb>c1) )
    uppind, = np.where( (wavea<c2) & (waveb>c2) )
    assert(len(lowind) <= 1)
    assert(len(uppind) <= 1)

    if (len(lowind) == 1) and (not (lowind in wholeind)):
      fracused[lowind] = (waveb[lowind]-c1)/pixwidth[lowind]
    if (len(uppind) == 1) and (not np.any(uppind in wholeind)):
      fracused[uppind] = (c2-wavea[uppind])/pixwidth[uppind]

    if check:
      plt.scatter(wavea, flux)
      plt.scatter(waveb, flux)
      plt.plot([c1,c1],[0,10])
      plt.plot([c2,c2],[0,10])
      print np.arange(0,len(flux))
      print fracused
      print flux
    
    integral = np.sum(flux*fracused*pixwidth)
    print integral
    if mean:
      return integral/np.sum(fracused*pixwidth)
    else:
      return integral
    
    
    
#    # loop over except first and last
#    totpix = 0.
#    totflux = 0.
#    integral = 0.
#    for i in range(len(wave)-2):
#      j = i+1
#      wvplus  = (wave[j] + wave[j+1])/2. # wave upper edge of pix
#      wvminus = (wave[j] + wave[j-1])/2. # wave lower edge of pix
#      pixwidth = (wvplus-wvminus)        # size of pixel
#      # full pixel
#      if (wvminus>c1) & (wvplus<c2):
#        frac = 1.
#      # partial pixel (lower region limit)
#      elif (wvminus<c1) & (wvplus>c1):
#        frac = (wvplus-c1)/pixwidth
#      # partial pixel (upper region limit)
#      elif (wvminus<c2) & (wvplus>c2):
#        frac = (wvplus-c2)/pixwidth
#      else:
#        frac = 0.
#        
#      if frac > 0:
#        totpix += frac
#        totflux += flux[j]*frac
#        integral += flux[j]*frac*pixwidth
#        if check:
#          print wave[j], frac, flux[j]
#        
#    if mean:
#      return totflux/totpix
#    else:
#      return integral
 
def simple_fracsum(wave, flux, c1, c2, mean=False):
  
    diff = np.array(wave.flat[1:] - wave.flat[:-1])
    pixwidth = np.concatenate(([diff[0]], (diff[1:]+diff[:-1])/2., [diff[-1]]))

    wavea = wave-pixwidth/2.
    waveb = wave+pixwidth/2.
   
    return fracsum(wavea, waveb, flux, c1, c2, mean=mean)


def test():

    wavea=np.arange(0,10)
    waveb=wavea+1.
    flux=np.ones_like(wavea)*2.
    flux[3:7]=4.
    c1 = 4.5
    c2=8.
    plt.clf()
    v1 = fracsum(wavea, waveb, flux, c1, c2, check=True)

    wave=np.arange(0,10)+0.5
    v2 = simple_fracsum(wave,flux, c1, c2)
    
    assert(v1 == v2)
    assert(v1 == 12.)
  
  
# Lithium index
def measure_li(wave, flux, trapz=False):

    fcen = 6707.8 # 6707.76; 6707.91
    # note iron at 6707.4
    fwid = 2.
    feature = [fcen-fwid/2.,fcen+fwid/2.]

    feat = simple_fracsum(wave, flux, feature[0], feature[1], mean=True)

    cont = simple_fracsum(wave, flux, 6710., 6712., mean=True)
    
    return feat/cont


# H alpha EW     
def measure_ha(wave, flux, trapsum=False):
    
    # feature region
    fcen = 6562.8
    fwid = 8.
    feature = [fcen-fwid/2.,fcen+fwid/2.]
    
    m1 = fracsum(wave, flux, 6500., 6550., mean=True)
    m2 = fracsum(wave, flux, 6575., 6625., mean=True)
    pseudo = (m1+m2)/2.

    ew = simple_fracsum(wave, 1.-flux/pseudo, feature[0], feature[1])
    return ew


def bandstrength(wave, flux, num, denom):
    
    num = simple_fracsum(wave, flux, num[0], num[1], mean=True)
    denom = simple_fracsum(wave, flux, denom[0], denom[1], mean=True)

    if (num is not None) & (denom is not None):
        return num/denom
    else:
        return None
    
def measure_lepine(wave, flux):
    
    CaH2	= bandstrength(wave, flux, [6814,6846], [7042,7046])
    
    CaH3	= bandstrength(wave, flux, [6960,6990], [7042,7046])	
    
    TiO5	= bandstrength(wave, flux, [7126,7135], [7042,7046])
    
    VO1	= bandstrength(wave, flux, [7430,7470], [7550,7570])
    
    TiO6	= bandstrength(wave, flux, [7550,7570], [7745,7765])
    
    VO2	= bandstrength(wave, flux, [7920,7960], [8130,8150])
    
    return CaH2, CaH3, TiO5, VO1, TiO6, VO2
