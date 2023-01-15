#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gdal
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import mesh_utilities as mesh

matplotlib.rcParams['xtick.direction']='out'
matplotlib.rcParams['ytick.direction']='out'
matplotlib.rcParams['axes.labelsize']='18'
matplotlib.rcParams['xtick.labelsize']='18'
matplotlib.rcParams['ytick.labelsize']='18'
matplotlib.rcParams['legend.fontsize']='18'
matplotlib.rcParams['font.family']='serif'
matplotlib.rcParams['font.sans-serif']='Times'


def get_map(natural_earth_file=None):
    """
    zmap: elevation espessed in rgb scale 0-255 for plotting purposing only 
    usage: plt.imshow(zmap, extent=[-180,180,-90,90])

    """

    if natural_earth_file == None:
        data = "/work/tonini/data"
        natural_earth_file = os.path.join(data, 
                                 'NE1_HR_LC_SR_W_DR/NE1_HR_LC_SR_W_DR.tif')

    ds = gdal.Open(natural_earth_file)
    data = ds.ReadAsArray()
    zmap = np.moveaxis(data, 0, -1)
    return zmap




def plot_mesh_abaqus(mesh_path, mesh_name):

    mesh_d = mesh.read_abaqus(mesh_path, mesh_name)
    polygons = mesh.create_polygons(mesh_d)
    

    xmin = np.amin(polygons[:,:,0])
    xmax = np.amax(polygons[:,:,0])
    ymin = np.amin(polygons[:,:,1])
    ymax = np.amax(polygons[:,:,1])

    n_polygons = len(polygons[:,:,0])
    plt.figure(figsize=(16,16))
    plt.grid(True)
    zmap = get_map()
    plt.imshow(zmap, extent=[-180,180,-90,90])

    for i in range(n_polygons):
        plt.fill(np.append(polygons[i,:,0], polygons[i,0,0]), 
                 np.append(polygons[i,:,1], polygons[i,0,1]), 
                 fill=False, color="#333333", linewidth=1)

    # plt.legend()
    # plt.title(name)
    plt.xlabel(r"Longitude ($^\circ$)")
    plt.ylabel(r"Latitude ($^\circ$)")
    plt.axis("equal")
    plt.xlim(xmin-1, xmax+1)
    plt.ylim(ymin-1, ymax+1)
    fileout = os.path.join(mesh_path, mesh_name + "_mesh.png")
    plt.savefig(fileout, fmt="png", bbox_inches="tight", dpi=150)
    plt.close()



def main():
    """

    """
    mesh_path = sys.argv[1]
    mesh_name = sys.argv[2]
    plot_mesh_abaqus(mesh_path, mesh_name)

if __name__ == "__main__":
    main()


