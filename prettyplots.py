import matplotlib as mpl
import matplotlib.pyplot as plt
import palettable
#from palettable.colorbrewer.sequential import Blues_8_r as Blues_r
from cycler import cycler

# make lines ticker and font bigger for everything
mpl.rc('lines',linewidth = 1.5)
mpl.rc('font',size = 12)
mpl.rc('axes',labelsize = 14, linewidth=1.25)
mpl.rc('xtick',labelsize = 14)
mpl.rc('ytick',labelsize = 14)
# enable math fonts
mpl.rc('mathtext', default = 'regular')

# this changes the default color cycle for line plots (not scatter plots though)
plt.rc('axes', prop_cycle=(cycler('color', palettable.colorbrewer.qualitative.Dark2_8.mpl_colors)))

# for scatter plots
global colors
colors = palettable.colorbrewer.qualitative.Dark2_3.mpl_colors

print colors