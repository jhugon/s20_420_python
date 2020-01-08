#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

def compare_results(results_names,results_values,results_uncertainties,accepted_value,accepted_uncertainty,results_label,output_image_name,space_for_result_names=0.3):

  if len(results_names) != len(results_values):
    error_message = "results_names should be the same length as results_values, but their lengths are: {} and {}. Exiting.".format(len(results_names),len(results_values))
    raise Exception(error_message)

  if len(results_names) != len(results_uncertainties):
    error_message = "results_names should be the same length as results_uncertainties, but their lengths are: {} and {}. Exiting.".format(len(results_names),len(results_uncertainties))
    raise Exception(error_message)
  
  fig, ax = plt.subplots(figsize=[5,5],gridspec_kw={'left':space_for_result_names,'right':0.95,'top':0.95})
  print(ax.margins())
  ax.margins(y=0.5)
  print(ax.margins())
  ax.axvspan(accepted_value-accepted_uncertainty,accepted_value+accepted_uncertainty,fc='c')
  ax.axvline(accepted_value,c='k',ls="-")
  ax.errorbar(results_values,results_names,xerr=results_uncertainties,fmt="ob")
  ax.set_xlabel(results_label)
  print(ax.margins())
  fig.savefig(output_image_name)
  
  for i in range(1,10):
    fig, ax = plt.subplots(figsize=[5,5],gridspec_kw={'left':space_for_result_names,'right':0.95,'top':0.95})
    if i == 1:
      ax.set_ylim(-0.05,0.05)
    ax.margins(y=0.2)
    ax.axvspan(1.5,1.9,fc='c')
    ax.axvline(1.7,c='k',ls="-")
    ax.errorbar([1.]*i,[str(j) for j in range(1,i+1)],xerr=0.5,fmt="ob")
    ax.set_xlabel(results_label)
    print(i,ax.get_ylim())
    fig.savefig("test{:0d}.png".format(i))
    plt.close()

#######################################
### This is just testing ##############
#######################################

if __name__ == "__main__":

  results_label = "Energy [eV]"
  
  results_names = [
  "Hugon, et. al.",
  "Dixon, et. al.",
  ]
  
  results_values = [
  1.2,
  1.28,
  ]
  
  results_uncertainties = [
  0.1,
  0.2,
  ]
  
  accepted_value = 1.5
  accepted_uncertainty = 0.05
  
  ## Increase this if your result name doesn't fit in the image
  ## Decrease if there is a ton of white space on the left of the image
  ## This is fraction of the image to be used for the result names
  space_for_result_names = 0.3
  
  output_image_name = "final_results.png"
  
  compare_results(results_names,results_values,results_uncertainties,accepted_value,accepted_uncertainty,results_label,output_image_name)
