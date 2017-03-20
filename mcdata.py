# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 14:10:51 2015

@author: enewton
"""
import numpy as np
import confidence 
import scipy.stats as stats
import matplotlib.pyplot as plt


def select(x, xerr=None, indices=None, replace=True, size=None):
    
    if size is None:
        size = len(x)

    if indices is None:
        indices = np.random.choice(np.arange(len(x)), size=size, replace=replace)

    if xerr is not None:
        xerr = np.zeros_like(x)+xerr
        x_re = [ np.random.normal(loc=x[i], scale=xerr[i], size=None) for i in indices]
    else:
        x_re = x[indices]
    return x_re

def select_xy(x, y, xerr=None, yerr=None, resample=True, replace=True):

    if resample: # bootstrap?
        indices = np.random.choice(np.arange(len(x)), size=len(x), replace=replace) 
    else: # keep original data
        indices = np.arange(len(x))
    try:
        xerr = np.zeros_like(x)+xerr
    except:
        pass
    try:
        yerr = np.zeros_like(y)+yerr
    except:
        pass
    x_re = select(x, xerr, indices=indices)
    y_re = select(y, yerr, indices=indices)
    
    return x_re, y_re
    
def mcspearman(x, y, xerr=None, yerr=None, resample=True, replace=True, nsamples=1000, debug=False):
    print nsamples
    correlation = np.zeros(int(nsamples))
    pvalues = np.zeros(int(nsamples))
    for i in np.arange(nsamples):

        x_re, y_re = select_xy(x,y, xerr=xerr, yerr=yerr, resample=resample, replace=replace)
        corr, pval = stats.spearmanr(x_re, y_re)
        correlation[i] = corr
        pvalues[i] = pval
        if debug and (np.mod(i,100) == 0):
            plt.scatter(x, y)
            plt.scatter(x_re, y_re, edgecolor='r', facecolor='None')
            print corr, pval
            plt.show()
    out = confidence.interval(correlation, interval=0.68)   
    out2 = confidence.interval(pvalues, interval=0.68)   
    return out, out2

def mcanderson(x, y, err=None, xerr=None, yerr=None, resample=True, replace=True, nsamples=1000, debug=False):
    
    if err is not None:
        xerr=err
        yerr=err
    statistic = np.zeros(nsamples)
    pvalue = np.zeros(nsamples)
    for i in np.arange(nsamples):
        
        if resample:
            x_re = select(x, xerr, replace=replace)
            y_re = select(y, yerr, replace=replace)
        else:
            x_re = select(x, xerr, replace=replace, indices=np.arange(len(x)))
            y_re = select(y, yerr, replace=replace, indices=np.arange(len(y)))
            
        stat, _, per = stats.anderson_ksamp([x_re, y_re]) 
        statistic[i] = stat
        pvalue[i] = per
        if debug and (np.mod(i,100) == 0):
            a=plt.hist(y_re)
            b=plt.hist(x_re)
            print stat, per
            plt.show()
    out = confidence.interval(statistic, interval=0.68)   
    out2 = confidence.interval(pvalue, interval=0.68)   
    return out, out2
        

        