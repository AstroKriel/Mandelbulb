## load modules
import os
import numpy as np
import multiprocessing as mp
import matplotlib.pyplot as plt
from pylab import cm

def plotDensity(var_iter, folder_data, filepath_dist_data, filepath_light_data):
    ## dimensions of the figure
    x_dim = 3.0
    y_dim = 3.0
    ## load distance data
    data_dist = np.genfromtxt(folder_data+filepath_dist_data, delimiter=',')
    ## load light data
    data_light = np.genfromtxt(folder_data+filepath_light_data, delimiter=',')
    ## plot and save image with desired aspect ratio 
    data = data_dist + data_light
    ## create figure
    fig = plt.figure(frameon=False)
    fig.set_size_inches(x_dim, y_dim)
    ax = plt.Axes(fig, [0.0, 0.0, 1.0, 1.0], )
    ax.set_axis_off()
    fig.add_axes(ax)
    ## plot distance data
    plt.imshow(data_dist, origin='lower', extent=[0, x_dim, 0, y_dim], cmap=cm.gray)
    plt.savefig('images/dist_'+str(var_iter).zfill(3)+'.png', dpi=300)
    ## plot light data
    plt.imshow(data_light, origin='lower', extent=[0, x_dim, 0, y_dim], cmap=cm.gray)
    plt.savefig('images/light_'+str(var_iter).zfill(3)+'.png', dpi=300)
    ## plot mixed data
    plt.imshow(data, origin='lower', extent=[0, x_dim, 0, y_dim], cmap=cm.gray)
    plt.savefig('images/mandelbulb_'+str(var_iter).zfill(3)+'.png', dpi=300)
    ## close figure
    plt.close()

if __name__ == '__main__':
    ## close all previously opened figure
    plt.close('all')
    ## get list of all data files
    folder_data = './data/'
    filepaths_dist_data  = sorted([filename for filename in os.listdir(folder_data) if filename.startswith("dist_")])
    filepaths_light_data = sorted([filename for filename in os.listdir(folder_data) if filename.startswith("light_")])
    filepaths_dist_data  = filepaths_dist_data[::3]
    filepaths_light_data = filepaths_light_data[::3]
    ## render images
    pool = mp.Pool()
    results = [pool.apply_async(plotDensity, 
        args=(var_iter, folder_data, filepaths_dist_data[var_iter], filepaths_light_data[var_iter],))
        for var_iter in range(len(min(filepaths_dist_data, filepaths_light_data)))]
    results = [p.get() for p in results] ## need to extract info for parallel process to run properly
    ## animate plots
    if len(min(filepaths_dist_data, filepaths_light_data)) > 10:
        os.system('ffmpeg -start_number 0 -i .\images\mandelbulb_%03d.png -vb 40M -framerate 40 -vf scale=1440:-1 -vcodec mpeg4 mandelbulb.mp4')
