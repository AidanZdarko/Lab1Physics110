import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Use the yi array to input your launch heights:
yi = np.array([0.303, 0.363, 0.427, 0.512, 0.634, 0.717])

# Use the xf array to input the xf values you measure:
xf = np.array([[0.715, 0.725, 0.715],
               [0.805, 0.823, 0.810],
               [0.881, 0.867, 0.873],
               [0.970, 0.996, 0.987],
               [1.034, 1.060, 1.056],
               [1.163, 1.160, 1.145]])

# Gravitational acceleration near the surface of the Earth
g = 9.8

# The following is the function from the end of the theory section.
# Inputing launch height (h) and horizontal velocity (v) returns
# the horizontal distance travelled: 
def x_dist(h,v):
    return v*((2*h/g)**.5)

# xf_avg is the average distance travelled from each launch height
xf_avg = np.mean(xf, axis=1)

# xf_min and xf_max contain the minimum and maximum results for
# each trial
xf_min = np.min(xf, axis=1)
xf_max = np.max(xf, axis=1)

# xf_aUnc is the absolute uncertainty of each trial calculated using
# maximum deviation.
xf_aUnc = np.array([xf_max-xf_avg, xf_avg-xf_min])
xf_aUnc = np.max(xf_aUnc, axis=0)

# xf_rUnc is the relative uncertainty of each trial. 
xf_rUnc = xf_aUnc/xf_avg

# rUnc_max is the largest value of any of the relative uncertainties
rUnc_max = np.max(xf_rUnc)

# Here, horizontal velocity is calculated by fitting the data from the
# experiment to curve from the theory section
vix, acc = curve_fit(x_dist, yi, xf_avg)

# Absolute uncertainty of the horizontal velocity is found by
# multiplying the largest relative uncertainty of the measurements
# by the calculated value for horizontal velocity.
vix_aUnc = rUnc_max*vix

print('Muzzle speed is', vix, 'plus/minus', vix_aUnc, 'm/s')

# These are arrays generated to graph the best fit line
yi_samp = np.linspace(np.min(yi)*.9,np.max(yi)*1.1,30)
xf_samp = x_dist(yi_samp,vix)

# Plotting the data
plt.plot(yi, xf_avg, 'o')
plt.plot(yi_samp, xf_samp)
plt.xlabel('initial height (m)')
plt.ylabel('horizontal distance (m)')
plt.show()

# Saving the data to csv files for use elsewhere. 
points = np.column_stack((yi,xf_avg))
best_fit = np.column_stack((yi_samp, xf_samp))

np.savetxt('bestFit.csv', best_fit, delimiter=',')
np.savetxt('points.csv', points, delimiter=',')