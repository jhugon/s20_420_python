#!/usr/bin/env python3

import scipy
import scipy.stats

def linearFit(x,y,printinfo=True):
    """
    Returns slope, intercept, slope error, intercept error, y error

    All from https://en.wikipedia.org/wiki/Simple_linear_regression
    on 2019-08-26

    Useage:

        if you have 1D arrays of x and y values in variables x and y:
        call like:

        slope, intercept, slopeerror, intercepterror, yerr = linearFit(x,y)
        
    """

    if len(x) != len(y):
        raise Exception("Length of x and y data must be the same!")

    x = scipy.array(x)
    y = scipy.array(y)
    N = len(x)
    meanx = scipy.mean(x)
    meany = scipy.mean(y)
    variancex = sum((x-meanx)**2)
    variancey = sum((y-meany)**2)
    covariance = sum((x-meanx)*(y-meany))

    slope = covariance / variancex
    intercept = meany - meanx*slope
    r2 = covariance**2 / variancex / variancey

    residuals = y - (slope*x+intercept)
    yvariance = sum(residuals**2/(N-2))

    slopevariance = yvariance/variancex
    interceptvariance = slopevariance * sum(x**2 / N)
    
    slopeerror = scipy.sqrt(slopevariance)
    intercepterror = scipy.sqrt(interceptvariance)
    yerr = scipy.sqrt(yvariance)

    if printinfo:
      onesigtailProb = scipy.stats.norm.sf(1)
      up1sigChiVal = scipy.stats.chi.ppf(onesigtailProb,df=N-2)
      down1sigChiVal = scipy.stats.chi.isf(onesigtailProb,df=N-2)
      yerrupBound =  yerr*(scipy.sqrt(N-2)/up1sigChiVal - 1)
      yerrdownBound =  yerr*(1 - scipy.sqrt(N-2)/down1sigChiVal)
      #yerrupBound =  scipy.sqrt(N-2)*yerr/up1sigChiVal
      #yerrdownBound =  scipy.sqrt(N-2)*yerr/down1sigChiVal
      #print(onesigtailProb)
      #print(up1sigChiVal)
      #print(down1sigChiVal)
      print("#"*80)
      print("Linear Fit Results for {} Data Points".format(N))
      print("slope estimate:               {:10.5g} +/- {:10.5g}".format(slope,slopeerror))
      print("intercept estimate:           {:10.5g} +/- {:10.5g}".format(intercept,intercepterror))
      print("y point uncertainty estimate: {:10.5g}   +{:<10.5g} -{:<10.5g}".format(yerr,yerrupBound,yerrdownBound))
      print("r^2:                          {:10.5g}".format(r2))
      print("#"*80)

    return slope, intercept, slopeerror, intercepterror, yerr

if __name__ == "__main__":

    #####################################
    ###### Testing the fit ##############
    #####################################

    from matplotlib import pyplot as plt
    from scipy import *

    Ntries = 1000
    Npoints = 15
    slopetrue = 1.45
    intercepttrue = 5.4
    errortrue = 10.
    x = linspace(0,100,Npoints)
    ytrue = slopetrue*x + intercepttrue

    slopezs = []
    interceptzs = []
    yerrratio = []
    for i in range(Ntries):
      yobs = ytrue + randn(len(x))*errortrue
      #plt.plot(x,yobs,".k")
      #plt.plot(x,ytrue,":b")
      #plt.savefig("data.png")
      slope, intercept, slopeerror, intercepterror, yerr = linearFit(x,yobs)
      slopezs.append((slope-slopetrue)/slopeerror)
      interceptzs.append((intercept-intercepttrue)/intercepterror)
      yerrratio.append(yerr**2/errortrue**2)
      plt.clf()

    title = "Simple Linear Regression for N={}, m={:.2f}, b={:.2f}, $\sigma_y$={:.2f}".format(Npoints,slopetrue,intercepttrue,errortrue)
    plt.hist(slopezs,bins=100,range=(-10,10),label="Data")
    plt.plot(linspace(-10,10,1000),scipy.stats.t.pdf(linspace(-10,10,1000),df=Npoints-2)*Ntries/5,label="t")
    plt.plot(linspace(-10,10,1000),scipy.stats.norm.pdf(linspace(-10,10,1000))*Ntries/5,label="Gaussian")
    plt.xlabel("Slope z-score")
    plt.ylabel("Trials / bin")
    plt.legend()
    plt.suptitle(title)
    plt.savefig("slope.png")
    plt.clf()
    plt.hist(interceptzs,bins=100,range=(-10,10),label="Data")
    plt.plot(linspace(-10,10,1000),scipy.stats.t.pdf(linspace(-10,10,1000),df=Npoints-2)*Ntries/5,label="t")
    plt.plot(linspace(-10,10,1000),scipy.stats.norm.pdf(linspace(-10,10,1000))*Ntries/5,label="Gaussian")
    plt.xlabel("Intercept z-score")
    plt.ylabel("Trials / bin")
    plt.suptitle(title)
    plt.legend()
    plt.savefig("intercept.png")
    plt.clf()
    plt.hist(yerrratio,bins=50,range=(0,5),label="Data")
    plt.plot(linspace(0,5,1000),scipy.stats.chi2.pdf(linspace(0,5*(Npoints-2),1000),df=Npoints-2)*(Ntries*(5*(Npoints-2))/50),label=r"$\chi^2/(N-2)$")
    plt.xlabel("y-Variance estimate / True Variance")
    plt.ylabel("Trials / bin")
    plt.suptitle(title)
    plt.legend()
    plt.savefig("yerr.png")
    plt.clf()

    plt.plot(arange(1000),(scipy.stats.t.sf(-1,arange(1000))-scipy.stats.t.cdf(-1,arange(1000)))/(scipy.stats.norm.sf(-1)-scipy.stats.norm.cdf(-1)))
    plt.xlabel("Number of data points")
    plt.ylabel("Ratio of t/Gaussian $\pm 1 \sigma$ Coverage")
    plt.xlim(0,30)
    plt.ylim(0.85,1.0)
    plt.savefig("tdist.png")
    plt.clf()

    meanslopez = mean(slopezs)
    meaninterceptz = mean(interceptzs)
    meanyerrratio = mean(yerrratio)
    stdslopez = std(slopezs)
    stdinterceptz = std(interceptzs)
    stdyerrratio = std(yerrratio)
    print("mean: slope: {:.3f}, intercept: {:.3f}, yerr: {:.3f}".format(meanslopez,meaninterceptz,meanyerrratio))
    print("std: slope: {:.3f}, intercept: {:.3f}, yerr: {:.3f}".format(stdslopez,stdinterceptz,stdyerrratio))

