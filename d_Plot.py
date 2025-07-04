""" 
Description: Visualization script to see plots of M1, M2, M3

History:
> Created by Jaime Uy De Baron 2025-01
"""
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

""" READ ME
    
    THIS FILE:
    # Plots visualizations of M1, M2, and M3
    
    USAGE NOTES:
    # Use Main.py User debug/modularization interface to identify what data you are plotting.
        # Deactivate the inputUI and writeOn booleans in Main.py - this makes it easier and more straightforward for visualization
            # but you will need to manually uncomment whichever specimen you are using in b_specimen.py...
            # And you will need to specify 'selected method = 3'
        # However, if you want to visualize with the full UI process, reactivate inputUI and writeOn booleans. 
        But you will need to use M3
"""

"""        # You must use M3 when GUI comes up
"""
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

""" User debug/modularization interface
    Turn parts of the code on and off for visualization (without the need to comment things out)
"""

import matplotlib.pyplot as plt # For plotting planes
import numpy as np # For array calculations
import numpy as np

# Plotting
plotAll = True # Make 'False' if want to turn off plots
plotM1 = True # Make 'False' if want to turn off M1 plot
plotM2 = True # Make 'False' if want to turn off M2 plot
plotM3 = True # Make 'False' if want to turn off M3 plot
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------


import matplotlib.pyplot as plt # For plotting planes
import numpy as np # For array calculations

from Main import S1, S2, S3, F1, dmatrix, bisection, M1npPlnCoeff, M2npPlnCoeff, M3npPlnCoeff, CalcM2
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

""" Plotting admin """

if plotAll:
    # Creating plot
    fig = plt.figure(figsize = (12,12))
    ax = fig.add_subplot(projection='3d')

    # Creating array for plotting curves
    z_new1 = np.linspace(S1.ztup[0], S1.ztup[-1], 100)
    x_new1 = S1.XfromZequ(z_new1) # Creating x's from x's
    y_new1 = S1.YfromZequ(z_new1) # creating y's from z's
    ax.scatter(CalcM2.endPointS1[0], CalcM2.endPointS1[1], CalcM2.endPointS1[2])
    ax.scatter(CalcM2.endPointS2[0], CalcM2.endPointS2[1], CalcM2.endPointS2[2])
    
    z_new2 = np.linspace(S2.ztup[0], S2.ztup[-1], 100)
    x_new2 = S2.XfromZequ(z_new2)
    y_new2 = S2.YfromZequ(z_new2)
    
    z_new3 = np.linspace(S3.ztup[0], S3.ztup[-1], 100)
    x_new3 = S3.XfromZequ(z_new3)
    y_new3 = S3.YfromZequ(z_new3)

    # Plotting fiducial reference point and curves
    ax.scatter(F1.xtup,F1.ytup,F1.ztup, c="g") # Fiducial location from 3DSlicer
    ax.plot(x_new1, y_new1, z_new1, c="r", label="Curve Fit to File 1") # Polynomial fitted
    ax.plot(x_new2, y_new2, z_new2, c="k", label="Curve Fit to File 2") # Polynomial fitted
    ax.plot(x_new3, y_new3, z_new3, c="b", label="Curve Fit to File 3") # Polynomial fitted

    # Plotting intersection points calculated
    ax.scatter(S1.intx,S1.inty,S1.intz, label="Intersection Points Curve 1")
    ax.scatter(S2.intx,S2.inty,S2.intz, label="Intersection Points Curve 2")

    # # Scatter plot for midpoints
    # concave_mid_x = npmidpoints[:, 0]
    # concave_mid_y = npmidpoints[:, 1]
    # concave_mid_z = npmidpoints[:, 2]

    # # Plot midpoints
    # ax.scatter(
    #     concave_mid_x, concave_mid_y, concave_mid_z, 
    #     color='blue', label='Method 2 Midpoints', s=80
    # )

    # Axes labels
    ax.set_xlabel('X-axis label')
    ax.set_ylabel('Y-axis label')
    ax.set_zlabel('Z-axis label')
    for labeli in plt.gca().axes.get_xticklabels():
        labeli.set_visible(False)
    for labeli in plt.gca().axes.get_yticklabels():
        labeli.set_visible(False)
    for labeli in plt.gca().axes.get_zticklabels():
        labeli.set_visible(False)
    ax.grid(False)
    ax.set_axis_off()
    ax.set_title('Histology Assignment Planes From {} Bisection'.format(bisection))

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

""" Plot method 1 """

if plotM1:
    # For plotting planes in python - note this is just biseciton planes, it DOES NOT have a microtomb offset
    size_plane = 4 # how many points will there be to define the planes?
    xx_arr = np.zeros((len(dmatrix), size_plane, size_plane))
    yy_arr = np.zeros((len(dmatrix), size_plane, size_plane))
    zz_arr = np.zeros((len(dmatrix), size_plane, size_plane))

    for i in range(len(dmatrix)):
        # Plotting plane
        # Define the plane equation coefficients for each plane (a, b, c, d)
        apl, bpl, cpl, dpl = M1npPlnCoeff[i][0], M1npPlnCoeff[i][1], M1npPlnCoeff[i][2], M1npPlnCoeff[i][3]  # Replace with your coefficients

        # Generate an array of grid of points
        x_vals = np.linspace(S1.intersec[i][0] - 15, S1.intersec[i][0] + 15, size_plane)
        y_vals = np.linspace(S1.intersec[i][1] - 15, S1.intersec[i][1] + 15, size_plane)
        xx, yy = np.meshgrid(x_vals, y_vals)

        # Calculate z values for each point on the grid using the plane equation
        zz = (-apl * xx - bpl * yy - dpl) / cpl

        # Appending np plane array
        xx_arr[i,:] = xx
        yy_arr[i,:] = yy
        zz_arr[i,:] = zz

    # Plotting each surface
    for p in range(len(dmatrix)):
        surf = ax.plot_surface(xx_arr[p], yy_arr[p], zz_arr[p], cmap = plt.cm.cividis)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

""" Plotting method 2 """

if plotM2:
    # Define the number of points for the grid
    size_plane = 4
    xx_arr_m2 = np.zeros((len(M2npPlnCoeff), size_plane, size_plane))
    yy_arr_m2 = np.zeros((len(M2npPlnCoeff), size_plane, size_plane))
    zz_arr_m2 = np.zeros((len(M2npPlnCoeff), size_plane, size_plane))

    for i in range(len(M2npPlnCoeff)):
        # Extract plane coefficients
        a_m2, b_m2, c_m2, d_m2 = M2npPlnCoeff[i]
        
        # Generate grid points
        x_vals_m2 = np.linspace(S2.intersec[i][0] - 15, S2.intersec[i][0] + 15, size_plane)
        y_vals_m2 = np.linspace(S2.intersec[i][1] - 15, S2.intersec[i][1] + 15, size_plane)
        xx_m2, yy_m2 = np.meshgrid(x_vals_m2, y_vals_m2)
        
        # Compute z values with error handling for c_m2 == 0
        if np.isclose(c_m2, 0):
            zz_m2 = np.full_like(xx_m2, np.nan)  # Or handle as a constant plane
            print(f"Skipping plane {i}: c_m2 is zero, parallel to xy-plane.")
        else:
            zz_m2 = (-a_m2 * xx_m2 - b_m2 * yy_m2 - d_m2) / c_m2

        # Append arrays for plotting
        xx_arr_m2[i, :] = xx_m2
        yy_arr_m2[i, :] = yy_m2
        zz_arr_m2[i, :] = zz_m2

    # Plot Method 2 planes
    for p in range(len(M2npPlnCoeff)):
        # Plot the surface
        surf_m2 = ax.plot_surface(
            xx_arr_m2[p], yy_arr_m2[p], zz_arr_m2[p], 
            alpha=0.6, cmap=plt.cm.coolwarm, label=f"Method 2 Plane {p+1}"
        )

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

""" Plotting method 3 """

if plotM3:
    # Define the number of points for the grid
    size_plane = 4
    xx_arr_m3 = np.zeros((len(M3npPlnCoeff), size_plane, size_plane))
    yy_arr_m3 = np.zeros((len(M3npPlnCoeff), size_plane, size_plane))
    zz_arr_m3 = np.zeros((len(M3npPlnCoeff), size_plane, size_plane))
    
    # Plot mc intersection points
    ax.scatter(S3.intx,S3.inty,S3.intz, label="Intersection Points Curve 2")


    for i in range(len(M3npPlnCoeff)):
        # Extract plane coefficients
        a_m3, b_m3, c_m3, d_m3 = M3npPlnCoeff[i]
        
        # Generate grid points
        x_vals_m3 = np.linspace(S3.intersec[i][0] - 15, S3.intersec[i][0] + 15, size_plane)
        y_vals_m3 = np.linspace(S3.intersec[i][1] - 15, S3.intersec[i][1] + 15, size_plane)
        xx_m3, yy_m3 = np.meshgrid(x_vals_m3, y_vals_m3)
        
        # Compute z values with error handling for c_m3 == 0
        if np.isclose(c_m3, 0):
            zz_m3 = np.full_like(xx_m3, np.nan)  # Or handle as a constant plane
            print(f"Skipping plane {i}: c_m2 is zero, parallel to xy-plane.")
        else:
            zz_m3 = (-a_m3 * xx_m3 - b_m3 * yy_m3 - d_m3) / c_m3

        # Append arrays for plotting
        xx_arr_m3[i, :] = xx_m3
        yy_arr_m3[i, :] = yy_m3
        zz_arr_m3[i, :] = zz_m3

    # Plot Method 3 planes
    for p in range(len(M3npPlnCoeff)):
        # Plot the surface
        surf_m3 = ax.plot_surface(
            xx_arr_m3[p], yy_arr_m3[p], zz_arr_m3[p], 
            alpha=0.6, cmap=plt.cm.viridis, label=f"Method 3 Plane {p+1}"
        )
    
        # Highlight the first plane with a marker
        if p == 0:
            center_x = np.mean(xx_arr_m3[p])
            center_y = np.mean(yy_arr_m3[p])
            center_z = np.mean(zz_arr_m3[p][~np.isnan(zz_arr_m3[p])])  # Avoid NaN issues
            
            ax.scatter(center_x, center_y, center_z, color='yellow', s=100, marker='o', label="First Plane Marker")

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ax.legend(False)

if plotAll:
    plt.gca().set_aspect('equal') # can remove to squash graph, but sets axis aspect ratio equal for visualisation...
    plt.show()