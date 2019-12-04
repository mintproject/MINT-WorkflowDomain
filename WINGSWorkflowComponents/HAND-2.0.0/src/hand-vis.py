## HAND discretised and visualised
## Daniel Hardesty Lewis

import rasterio as rio
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma
import argparse

def argparser():

    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--dd", type=str, help="")
    parser.add_argument("-c", "--cmap", type=str, help="")
    parser.add_argument("-b", "--bins", type=int, help="")
    parser.add_argument("-o", "--output", type=str, help="")

    args = parser.parse_args()

    if not args.dd:
        parser.error('-d --dd Distance down raster')
    if not args.cmap:
        parser.error('-c --cmap Name of Matplotlib colormap')
    if not args.bins:
        parser.error('-b --bins Number of bins for discretization')
    if not args.output:
        parser.error('-o --output Output PNG of distance down')

    return(args)

def main():
    options = argparser()

    basindd = rio.open(options.dd)
    basinddma = ma.array(basindd.read(),mask=(basindd.read()==basindd.nodata))
    #basinddma.fill_value = -1.
    basinddmasort = np.sort(ma.array(basinddma.data,mask=((basinddma.mask)|(basinddma.data==0.))).compressed())
    bins = options.bins
    basinddmasortbins = np.zeros(bins+1)
    basinddmasortbins[0] = basinddmasort.min()
    for i in range(1,bins+1):
        basinddmasortbins[i] = basinddmasort[round(len(basinddmasort)/float(bins)*float(i))-1]
    ## basinddmasort[round(len(basinddmasort)/7.*7)-1]==basinddmasort.max()==True
    #plt.hist(basinddmasort,bins=basinddmasortbins)
    #plt.show()
    ## "<=" in the first condition below
    ##  because we have intentionally excluded 0s as nodata values
    basinddmasortbinsmean = np.zeros(bins)
    basinddmasortbinsmean[0] = basinddmasort[(basinddmasortbins[0]<=basinddmasort)&(basinddmasort<=basinddmasortbins[1])].mean()
    for i in range(1,bins):
        basinddmasortbinsmean[i] = basinddmasort[(basinddmasortbins[i]<basinddmasort)&(basinddmasort<=basinddmasortbins[i+1])].mean()
    basinddmadigi = np.digitize(basinddma,basinddmasortbins,right=True)
    cmap = mpl.cm.get_cmap(options.cmap)
    cmapdiscretear = cmap(np.linspace(0,1,bins))
    for i in range(1,bins-1):
        cmapdiscretear[i] = np.append(cmap.colors[int(round(float(len(cmap.colors))/(basinddmasortbinsmean[bins-1]-basinddmasortbinsmean[0])*np.cumsum(np.diff(basinddmasortbinsmean))[i-1]))-1],1.)
    cmapdiscrete = mpl.colors.ListedColormap(cmapdiscretear)
    fig,ax = plt.subplots()
    cax = ax.imshow(basinddmadigi.squeeze(),interpolation='none',cmap=cmapdiscrete)
    ax.set_title('Vertical distance down to nearest drainage')
    cbar = fig.colorbar(cax)
    basinddmasortbinsstr = ['{:.2f}'.format(x) for x in basinddmasortbins.tolist()]
    cbar.ax.set_yticklabels([s + ' m' for s in basinddmasortbinsstr])
    plt.savefig(options.output)
    plt.show()

if __name__ == "__main__":
    main()

