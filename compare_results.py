#!/usr/bin/env python3

import sys
import matplotlib.pyplot as plt
import numpy as np

result_value_label = "Energy [eV]"

results_name = [
"Hugon, et. al.",
"Dixon, et. al.",
]

results_value = [
1.2,
1.28,
]

results_uncertainty = [
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

#######################################
#######################################
#######################################

if len(results_name) != len(results_value):
  print()
  sys.exit(1)

fig, ax = plt.subplots(figsize=[5,5],gridspec_kw={'left':space_for_result_names,'right':0.95,'top':0.95})
print(ax.margins())
ax.margins(y=0.5)
print(ax.margins())
ax.axvspan(accepted_value-accepted_uncertainty,accepted_value+accepted_uncertainty,fc='c')
ax.axvline(accepted_value,c='k',ls="-")
ax.errorbar(results_value,results_name,xerr=results_uncertainty,fmt="ob")
ax.set_xlabel(result_value_label)
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
  ax.set_xlabel(result_value_label)
  print(i,ax.get_ylim())
  fig.savefig("test{:0d}.png".format(i))
  plt.close()
