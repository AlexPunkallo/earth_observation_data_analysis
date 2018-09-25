from snappy import ProductIO  # SNAP package to interface SNAP with Python
import numpy as np  # Mathematical tool
import pandas as pd # Dataframe tool
import matplotlib.pyplot as plt # Data visualization tool
import seaborn as sns # Statistical data visualization tool
%matplotlib inline

# Image Subset path
subset = ProductIO.readProduct("/application/pi/Desktop/track1/Subset_S2A_MSI
L2A_20170411T100031_N0204_R122_T33TVH_20170411T100025BandMath_resampled.dim")

subset.getNumBands()  # Get the number of the bands
bands = [subset.getBandAt(i).getName() for i in 
         range(subset.getNumBands())] # Create a list of the bands names
mybands = bands[1:12]  # Take bands we need (from 1 to 11)
mybands.append("water") # Add also the "water" mask
print mybands

raster_data = {} # Create a dictionary (band name:data) to insert the band data

for band in mybands: # For every (considered) band name, do:
    band_data = subset.getBand(band)  # Get the band data from the image with 
                                    #that name
    w = band_data.getRasterWidth()  # Get the width
    h = band_data.getRasterHeight() # Get the height
    band_data_data = np.zeros(w * h, np.float32) # Create a matrix of 
                                                #zeros (n,m) = (width,height)
    band_data.readPixels(0, 0, w, h, band_data_data) # Read pixel values
    #band_data_data.shape = h, w        #optional, check indices of the matrix
    raster_data[band] = band_data_data # Insert the matrix in the dictionary
    
#print raster_data['B1']            # Ex. print band 1 values

bands_df = pd.DataFrame(raster_data) # Create a dataframe object with 
                                    #the band matrices
mask = bands_df.water.isnull() == False # Fix NaN values of the water mask

correl=bands_df[mask].corr(method='pearson', min_periods=1) # Computer the 
                        #correlation between the bands (Pearson method)

# Plot parameters
plt.rc("figure", figsize=(10, 8))
ax=sns.heatmap(correl, cmap='Reds', vmax=1.0, vmin=-1.0 , linewidths=2.5, 
        annot=True)
plt.yticks(rotation=0) 
plt.xticks(rotation=90)
#f,ax = plt.subplots(figsize=(11,9))
fig = ax.get_figure()
fig.savefig('correlation.png')
plt.show()