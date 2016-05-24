# -*- coding: utf-8 -*-
"""
confidence_interval:
    Calculates the confidence limits of an array based on
    user-provided interval. Returns lower, middle,
    and upper confidence limits (middle is the median).
    
Usage:
    import ernlib.confidence as confidence
    lower,middle,upper = confidence.interval(data)
    lower,middle,upper = confidence.interval(data, interval=85)
    
"""

import numpy as np

def interval(x,interval=0.95, verbose=0, force_finite=False):
    """ x is array-like
        interval may be given as a fraction or percent
        verbose is off by default """
        
    # safe to assume you don't want to .1% confidence interval
    if interval > 1: 
        interval = interval/100
        if verbose > 0: print "confidence_interval: interval greater than 1, assuming you meant percent"

    # catch NaNs?
    if not force_finite: ## remove them
        x2 = x[np.isfinite(x)]
        if verbose > 0: print "confidence.interval: removing any nans from your array. %i nans removed." % (x.size-x2.size)
    elif np.all(np.isfinite(x)): ## there are no nans
        x2 = x
    else:
        raise ValueError("NaNs in array, force_finite is set")
     
    n = x2.size

    left = int(round((1.0-interval)*n))
    middle = int(round(0.5*n))
    right = int(round((interval)*n))
    
    if right == n: 
        right = n-1
        if verbose > 0:
            print "confidence.interval: setting right limit to max of data."
    if middle == n:
        middle = n -1
        if verbose > 0:
            print "confidence.interval: setting middle limit to max of data."
    # hmm, this shouldn't really happen...

    y = sorted(x2)
    if verbose > 0: 
        print "confidence.interval: elements for low and upper confidenece limits are %i and %i" % (left, right)
        print "confidence.interval: element for median is %i" % middle
        print "confidence.interval: (left, middle, right) =" (left,middle,right)
    try:
        out = [y[left],y[middle],y[right]]
    except:
        print "confidence.interval: your array was size ", n, " and your interval was ", interval
        print left,middle,right
        raise
        
    return out