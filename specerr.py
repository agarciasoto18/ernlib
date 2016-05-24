# -*- coding: utf-8 -*-
"""
Created on Tue May 24 11:07:56 2016

@author: enewton
"""
import numpy as np
import ernlib.confidence as confidence
import matplotlib.pyplot as plt

# calculate a Gaussian
def gaussian(x, mu, sig):
  return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))


# generate a matrix with gaussians along the diagonal
# note this can get quite memory-intensive for large arrays
# and a more sophisticated method should be used.
def gen_cov(wave, fwhm):

  sz = len(wave)
  cov = np.zeros((sz,sz))
  y = gaussian(np.arange(sz), 0, fwhm)
  yr = gaussian(np.arange(sz, 0, -1), 0, fwhm)
  for i in range(sz):
      cov[0:i,i]=yr[sz-i:]
      cov[i:,i]=y[0:sz-i]
      
  return cov

# add error based on error on each point and the covariance matrix
def add_err(e_flux, cov):
  
  err = np.random.normal(scale=e_flux)
  return np.dot(err, cov) 

# Monte Carlo errors     
def mc(wave, flux, e_flux, 
       function, 
       niter=10,
       check=False,
       interval=68.,
       return_values=False,
       cov=False):

  if check:
    flux_arr = np.ndarray([niter,len(flux)]) 

  for i in np.arange(0,niter):
  
    if np.sum(cov):
      err = add_err(e_flux, cov)
      new_flux = np.array(flux)+err
    else:
      tmp = np.array(e_flux)
      tmp[e_flux<0.] = np.median(e_flux)
      new_flux = np.random.normal(loc=flux, scale=tmp)
      print "MC: Did not use covariance matrix."
      
    myfunction = globals()[function]  #Get the function
    vals = myfunction(wave, new_flux)
    if isinstance(vals, float):
      vals = [vals]
    
    if i == 0:
      vals_arr = np.ndarray([niter,len(vals)])
    else:# if MC trials....
      vals_arr[i,:] = vals
      if check:
        flux_arr[i,:] = new_flux
        plt.plot(wave, new_flux, c='k', alpha=0.3)
          
  if check:
#    flux_sig = np.std(flux_arr, axis=0)
    plt.errorbar(wave, flux, e_flux, c='r')    

  # calculate confidence limits and error array    
  conf = np.ndarray([len(vals),3])
  err = np.ndarray([len(vals)])

  for i in np.arange(len(vals)):
    if np.all(np.isfinite(vals_arr[:,i])):
      conf[i,:] = confidence.interval(vals_arr[:,i], 
                                               interval=interval)
      err[i] = (conf[i,2]-conf[i,0])/2.
    else:
      conf[i,:] = [np.nan, np.nan, np.nan]
      err[i] = np.nan
      
  if return_values:
      return vals_arr
  else:
      return err
