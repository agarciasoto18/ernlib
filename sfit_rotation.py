# -*- coding: utf-8 -*-
"""
Created on Wed Nov 19 15:28:41 2014

@author: enewton
"""
import sfit
import math
import numpy as np
import matplotlib.pyplot as plt

#####
def period(lc_dict, vbest=None):
    buf = prep_period(lc_dict)
    fit = fit_period(buf, vbest=vbest)
    for ilc, lc in enumerate(lc_dict['data']):
        cm = fit['ep'][ilc][0]
        try:
            fwhm = fit['ep'][ilc][1]
        except:
            fwhm = 0.
        single_fit = {'frequency':fit['frequency'],
                      'phase':fit['phase'][ilc],
                      'amplitude':fit['amplitude'][ilc],
                      'dc':[fit['dc'][ilc]],
                      'cm':cm,
                      'fwhm':fwhm}
        lc.update_model(single_fit)
    lc_dict['period'] = lc.period

#####
def prep_period(lc_dict):

    try:
        buf = [None]*len(lc_dict['data'])
        for ilc, lc in enumerate(lc_dict['data']):
            tmp = lc.prep_period()
            buf[ilc] = tmp[0]                
    except:
        buf = lc_dict['data'].prep_period()
        
    return buf
            
#####
# refit period
def fit_period(buffy, ftest=False, vbest=None, window=273., pmin=0.1, pmax=300., verbose=0):


    # Keep track of largest window for deciding frequency sampling.
    # Sampling in frequency (with oversampling).
    vsamp = 0.1 / window
      
    # Period range (frequency, oversampled)
    pl = int(math.floor(1.0 / (vsamp*pmax)))
    if pl < 1:
        pl = 1
    ph = int(math.ceil(1.0 / (vsamp*pmin)))
    # number of steps in between
    nn = ph-pl+1

    (chinull, bnull, covnull) = sfit.null(buffy) # null hypothesis

    nmodel = 0
    nnull = 0
    nmeas = 0
    # calculate the number of free parameters
    for i, buf in enumerate(buffy):
        (t, y, wt, ep, idc, iamp) = buf
        if ep is not None:
            nmodel += ep.shape[0]
        if idc is not None:
            nmodel += np.max(idc)+1
            nnull += np.max(idc)+1
        if iamp is not None: 
            nmodel += np.max(iamp)+1
            nnull += np.max(iamp)+1
        nmeas += len(t)
    if verbose >= 1:
        print "mearth_lc:fit_period: Number of parameters..."
        print "...........model: ", nmodel
        print "......null model: ", nnull
        print ".....data points: ", nmeas

    # if vbest is not supplied, do the search
    if vbest is None:    
        if verbose > 1:
            print "mearth_lc:fit_period: vbest not supplied, calculating."
        # Perform period search.
        (pergrm, winfunc) = sfit.search(buffy, pl, ph, vsamp)
        # Best period.
        p = np.argmin(pergrm)
        
        # Parabolic interpolation for a better estimate.
        if p > 0 and p < nn-1:
            aa = pergrm[p]
            bb = 0.5*(pergrm[p+1] - pergrm[p-1])
            cc = 0.5*(pergrm[p+1] + pergrm[p-1] - 2.0*aa)
            offset = -0.5*bb/cc
            
            if ftest:
                pergrm = np.array(pergrm)
                pergrm = (chinull/pergrm-1.)/(nmodel-nnull)*(nmeas-nmodel)
                aa = pergrm[p]
                bb = 0.5*(pergrm[p+1] - pergrm[p-1])
                cc = 0.5*(pergrm[p+1] + pergrm[p-1] - 2.0*aa)
                offset = -0.5*bb/cc
                if verbose > 1:
                    print "mearth_lc:fit_period: performed f-test instead of straight chi2"
        else:
            offset = 0.0
    # don't do the search if vbest is supplied        
    else:
        print "mearth_lc:fit_period: vbest supplied: ", vbest
        pergrm = 0
        winfunc = 0

    if np.all(np.isfinite(pergrm)):
        if vbest is None:
            vbest = (pl+p+offset)*vsamp # best frequency (1/days)
        (chialt, balt, covalt) = sfit.single(buffy, vbest) # single period hypothesis
    else:
        vbest = float('NaN')
        chialt = float('NaN')
        balt = float('NaN')
    
    if verbose>1: 
        print "mearth_lc:fit_period: Fitting successful, parameters = "
        print "          Best period", 1.0/vbest, "days"
    
    # Frequency grid for plot.
    v = np.linspace(pl, ph, nn)
    v *= vsamp
    
    # unpack the buffer
    nep = []
    ndc = []
    namp = []
    phase = []
    amp = []
    dc = []
    mep = []
    for i, buf in enumerate(buffy):
        (t, y, wt, ep, idc, iamp) = buf
        if ep is not None:
            if ep.ndim == 1: 
                my_nep = 1
            else:
                my_nep = ep.shape[0]
        else:
            my_nep = None
        nep.append(my_nep)
        if idc is not None:
            my_ndc = np.max(idc)+1
        else:
            my_ndc = None
        ndc.append(my_ndc)
        if iamp is not None: 
            my_namp = np.max(iamp)+1
        else:
            my_namp = None
        namp.append(my_namp)

        try:
            (bdc, bep, bsc)=unpack_model(balt[i],nep=my_nep,ndc=my_ndc,namp=my_namp)
        except:
            bep = float('NaN')
            bdc = float('NaN')
            bsc = [float('NaN'),float('NaN')]
        
        my_phase=math.atan(bsc[1]/bsc[0])
        if bsc[1] < 0 and bsc[0] < 0: my_phase = my_phase - math.pi
        if bsc[1] > 0 and bsc[0] < 0: my_phase = my_phase + math.pi
        phase.append(my_phase)
        my_amp = math.sqrt(bsc[0]**2 + bsc[1]**2)
        amp.append(my_amp)
        dc.append(bdc)
        mep.append(bep)
       
    # save dictionary of fitting results
    fit_dict = {'frequency':vbest,
                'periodogram':pergrm,'windowfunc':winfunc,'spacing':v,
                'model':balt, 'nullmodel':bnull,
                'chi':chialt, 'nullchi':chinull, 
                'cov':covalt, 'nullcov':covnull,
                'nep':nep, 'ndc':ndc, 'namp':namp,
                'phase':phase, 'amplitude':amp, 
                'ep':mep,'dc':dc}
    return fit_dict
     
  
#####
# Get the model parameters
def unpack_model(model, ep=None, idc=None, iamp=None, 
                 nep=None, ndc=None, namp=None, ampcov=False):
     
        b = model
        if ep is not None:
            nep = ep.shape[0]
        else:
            if nep is None: nep = 1
    
        if idc is not None:
            ndc = np.max(idc)+1
        else:
            if ndc is None: ndc = 0
    
        if iamp is not None:
            namp = np.max(iamp)+1
        else:
            if namp is None: namp = 0
    
        # model is covariance matrix
    
        if ampcov: 
            s1 = model[ndc+nep][ndc+nep+1]
            s2 = model[ndc+nep+1][ndc+nep]
            try:
                assert ( np.abs((s1 - s2)/s1) < 1e-6 ) 
            except:
                print s1, s2
                print np.abs((s1 - s2)/s1)
                s1 = np.NaN
            return s1

        # This is how the "b" array is packed.

        bdc = b[0:ndc]        # DCs
        bep = b[ndc:ndc+nep]  # external parameters
        bsc = b[ndc+nep:ndc+nep+2]     # sin, cos, sin, cos, ...

        return (bdc, bep, bsc)
   
#####
# Periodogram plot 
def plot_pgram(buffy, fit_dict, 
               alias=True,  ## plot aliases of best frequency?
               window=True,  ## plot window function?
               flux_ylim=False, ## force y limits for flux?
               title=False,
               labels=False,
               ftest=True,
               cmap=False): ## include plot title?
    
    model = fit_dict['model']
    pergrm = fit_dict['periodogram']
    winfunc = fit_dict['windowfunc']
    v = fit_dict['spacing']
    vbest = fit_dict['frequency']

    fc='none'
    ec='k'
    if cmap:
        ec = 'none'
    c='k'
                               
    # "Amplitude spectrum" equivalent is square root of chi^2.
    ampspec = np.sqrt(pergrm)
    
    # Plot setup
    if window:
        npanel = len(buffy)+2
        amp_panel = npanel-1
    else:
        npanel = len(buffy)+1
        amp_panel = npanel
    pgram = plt.figure()
    pgram_ax = []
   
    # individual light curve plots
    for ilc, lc in enumerate(buffy):
        (t, y, wt, ep, idc, iamp) = lc
    
        (bdc, bep, bsc) = unpack_model(model[ilc], ep, idc, iamp)

        # phase and apply common mode, DC offsets
        phase = np.fmod(vbest*t, 1.0)
        if idc is None:
            blm = np.zeros(len(t))
        else:
            blm = bdc[idc] + np.dot(bep, ep)
    
        try:
            ylow = flux_ylim[0]
            yhigh = flux_ylim[1]
        except:
            ylow = np.max(y-blm)
            yhigh = np.min(y-blm)
        # plot data 
        if ilc==0:
            myplot = pgram.add_subplot(npanel, 1, ilc+1, 
                                   xlim=[0.0,1.0],
                                   ylim=[ylow,yhigh])
            if title:
                plt.title(title)
        elif ilc>0:
            myplot = pgram.add_subplot(npanel, 1, ilc+1, 
                                   xlim=[0.0,1.0],
                                   ylim=[ylow,yhigh],
                                   sharex=pgram_ax[0])

        pgram_ax.append(myplot)
        if cmap:
            myplot.scatter(phase, y-blm, marker='o',c=t,edgecolors=ec,alpha=0.6,cmap='nipy_spectral')
        else:
            myplot.scatter(phase, y-blm, marker='o',facecolors=fc,edgecolors=ec)
        
        # plot model
        modx = np.linspace(0.0, 1.0, 1000)
        modp = 2*math.pi*modx
        mody = bsc[0] * np.sin(modp) + bsc[1] * np.cos(modp)
        myplot.plot(modx, mody)
        if labels:
            myplot.set_ylabel('Magnitude')
            if ilc == (len(buffy)-1):
                myplot.set_xlabel('Phase')
  
        my_phase=math.atan(bsc[1]/bsc[0])
        if bsc[1] < 0 and bsc[0] < 0: my_phase = my_phase - math.pi
        if bsc[1] > 0 and bsc[0] < 0: my_phase = my_phase + math.pi
        y = math.sqrt(bsc[0]**2 + bsc[1]**2)*np.sin(modp + my_phase)

        myplot.plot(modx,y, color=c) 
        
#        phase = math.atan(bsc[1]/bsc[0])
#        if bsc[1]<0: phase = phase + math.pi
#        y = math.sqrt(bsc[0]**2 + bsc[1]**2)*np.sin(modp + phase)

    # now plots for all the data 
    if len(pgram_ax)>1: plt.setp([a.get_xticklabels() for a in pgram_ax[0:-1]], visible=False)

    # amplitude
    amp_plot = pgram.add_subplot(npanel, 1, amp_panel,
                                 xlim = [np.min(v), np.max(v)],
                                 ylim = [np.max(ampspec), np.min(ampspec)]) 
    amp_plot.set_xlim([np.min(v), np.max(v)])
    if ftest: ## ftest
        ampsorted = np.sort(ampspec)
        amp_plot.set_ylim([ampsorted[int(ampsorted.size*0.01)], np.max(ampspec)])
    else: ## chi2     
        amp_plot.set_ylim([np.median(ampspec), np.min(ampspec)])
    amp_plot.plot(v, ampspec, color=c)
    amp_plot.plot([vbest, vbest], plt.ylim(), linewidth=3, linestyle='--')
    if alias:
        for harm in np.arange(1,10):
            amp_plot.plot([vbest*harm,vbest*harm], plt.ylim(), linewidth=2, linestyle=':',color='k')
            amp_plot.plot([harm+(vbest),harm+(vbest)], plt.ylim(), linewidth=2, linestyle=':',color='r')
            amp_plot.plot([harm-(vbest),harm-(vbest)], plt.ylim(), linewidth=2, linestyle=':',color='r')
    amp_plot.text(0.95,0.8,'v = ' + str(vbest), ha='right',
                      transform=amp_plot.transAxes)
    if labels:
        amp_plot.set_ylabel('Amplitude')
        amp_plot.set_xlabel('Frequency')
   
    # window function
    if window:
        win_plot = pgram.add_subplot(npanel, 1, npanel,
                                    xlim = [np.min(v), np.max(v)],
                                    ylim = [0.0, 1.0], sharex=amp_plot)
        win_plot.plot(v, winfunc, color=c)
        win_plot.plot([vbest, vbest], plt.ylim(), linestyle='--')
        plt.setp(amp_plot.get_xticklabels(),visible=False)
    pgram.tight_layout()
    
    return pgram