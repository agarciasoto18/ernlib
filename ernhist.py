# -*- coding: utf-8 -*-
"""
Created on Thu May 28 08:09:41 2015

@author: enewton
"""

from sklearn.neighbors import KernelDensity
import numpy as np
import matplotlib.pyplot as plt

def onehist(arr,  # input array
            histtype='stepfilled', linestyle='solid',
            bins = 10,
            fill = False,
            frac = False, # plot as fraction of total
            kde = False, # plot as kernel density?
            bandwidth = 10, # kernel size
            xlim = None,
            stacked=False,
            **kwargs) :

  if xlim is None:
    xlim = [np.nanmin(arr),np.nanmax(arr)]
    
  if kde and not stacked:
    x_plot = np.linspace(xlim[0],xlim[1],1000)
    kde = KernelDensity(kernel='gaussian', bandwidth=bandwidth).fit(arr[np.isfinite(arr)].reshape(-1,1))
    log_dens = kde.score_samples(x_plot.reshape(-1,1))
    plt.plot(x_plot, np.exp(log_dens), 
             **kwargs)
  else:
    if isinstance(arr,list):
      weights = []
      for aa in arr:
        ww = np.ones_like(np.array(aa))
        if frac:
          ww = ww/len(np.array(aa))
        weights.append(ww)
    else:
      weights = np.ones_like(np.array(arr))
      if frac:
        weights = weights/len(np.array(arr))
    
    vals = plt.hist(arr, range=xlim, bins=bins, 
             histtype=histtype, linestyle=linestyle,
             weights=weights, fill=fill,
             stacked=stacked, **kwargs)
    
    return vals
  
  
def colhist(
        x, # array of values
        label = None, 
        samp = 0,
        nbins = 10,               # number of bins
        legend_loc = 'upper left', 
        fontsize = None,
        kde = False, bandwidth = 10, # kernel density estimator
        frac = False,           # plot fraction of total sample
        xlim=None, ylim=None,       # plot range
        short_ylabel=False,
        show_ylabel=False):

  # plot labels!    
  if short_ylabel:
    if frac:
        ylab = 'Frac. stars'
    else:
        ylab = 'No. stars'
  else:
    if frac:
        ylab = 'Fraction of stars'
    else:
        ylab = 'Number of stars'
  

  histtype = 'step'
  linestyle = 'solid'
  if samp == 1:
    fc = '#A4D8C9' #'#d9f8e0' #'#d9f8ef'
    ec = '#1b9e77'
    histtype = 'stepfilled'
  elif samp == 2:
    fc = '#cbdff0'
    ec = '#377eb7'
  elif samp == 3:
    fc = 'None'
    ec = '#d95f02'
    linestyle = 'dashed'
  else:
    fc = 'None'
    ec = 'k'
    linestyle = 'dotted'
    
    
  onehist(x,  # input array
          label, 
          histtype=histtype, linestyle=linestyle,
          ec = ec, fc = fc,
          nbins = nbins, 
          frac = frac, # plot as fraction of total
          kde = kde, # plot as kernel density?
          bandwidth = bandwidth, # kernel size
          xlim = xlim)     
    
  if np.all(xlim) is not None:
    plt.xlim(xlim)

  if np.all(ylim) is not None:
    plt.ylim(ylim)
  else:
    yr = plt.ylim() ## with error bars tends to go below 0
    plt.ylim(0,yr[1])
  
  if show_ylabel:
    plt.ylabel(ylab)
  
  if legend_loc is not False:
    if fontsize is not None:
      plt.legend(loc=legend_loc, prop={'size':fontsize})
    else:
      plt.legend(loc=legend_loc)
