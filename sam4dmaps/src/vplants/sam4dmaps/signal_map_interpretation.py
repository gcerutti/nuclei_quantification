import numpy as np
import scipy.ndimage as nd
from openalea.container import array_dict
from scipy.cluster.vq import vq

from vplants.sam4dmaps.sam_model import reference_meristem_model
from vplants.sam4dmaps.sam_model_registration import meristem_model_cylindrical_coordinates, meristem_model_organ_gap
from vplants.sam4dmaps.sam_map_construction import meristem_2d_cylindrical_map, draw_signal_map

from openalea.cellcomplex.mesh_oalab.widget.cute_plot import map_plot

from vplants.sam4dmaps.sam_model_tools import nuclei_density_function
from openalea.mesh.property_topomesh_creation import triangle_topomesh
from openalea.mesh import TriangularMesh
            
import matplotlib.pyplot as plt
import matplotlib.patches as patch
from openalea.oalab.colormap.colormap_def import load_colormaps


def local_extrema(signal, abscissa=None, scale=1, threshold=None):
    if abscissa is None:
        abscissa = np.arange(len(signal))
    
    distances = np.power(np.power(abscissa[np.newaxis] - abscissa[:,np.newaxis],2),0.5)
    
    maxima = np.ones_like(signal,bool)
    signal_neighborhood_max = np.array([np.max(signal[(distances[p]<=scale)&(distances[p]>0)]) for p in xrange(len(signal))])
    maxima = maxima & (signal > signal_neighborhood_max)
    maxima[0] = False
    maxima[-1] = False
    maximal_points = np.transpose([abscissa[maxima],signal[maxima]])
                     
    minima = np.ones_like(signal,bool)
    signal_neighborhood_min = np.array([np.min(signal[(distances[p]<=scale)&(distances[p]>0)]) for p in xrange(len(signal))])
    minima = minima & (signal < signal_neighborhood_min)
    minima[0] = False
    minima[-1] = False
    minimal_points = np.transpose([abscissa[minima],signal[minima]])
    
    return maximal_points, minimal_points


def extract_clv3_circle(positions, clv3_values, clv3_threshold=0.4, map_figure=None):
    if map_figure is None:
        map_figure = plt.figure(0)
        map_figure.clf()
    
    X = positions[:,0]
    Y = positions[:,1]
    data_range = [[-200,200],[-200,200]]
    xx, yy, zz = map_plot(map_figure,X,Y,clv3_values,XY_range=data_range,smooth_factor=1,n_points=100)
    resolution = np.array([xx[0,1]-xx[0,0],yy[1,0]-yy[0,0]])

    zz[np.isnan(zz)] = 0
                
    clv3_regions = nd.label((zz>clv3_threshold).astype(int))[0]
    components = np.unique(clv3_regions)[1:]
    component_centers = np.transpose([nd.sum(xx,clv3_regions,index=components),nd.sum(yy,clv3_regions,index=components)])/nd.sum(np.ones_like(xx),clv3_regions,index=components)[:,np.newaxis]
    
    if len(component_centers)>0:
        component_matching = vq(np.array([[0,0]]),component_centers)
        clv3_center = component_centers[component_matching[0][0]]
        clv3_area = (clv3_regions==component_matching[0]+1).sum() * np.prod(resolution)
        clv3_radius = np.sqrt(clv3_area/np.pi)

        c = patch.Circle(xy=clv3_center,radius=clv3_radius,ec="#c94389",fc='None',lw=3,alpha=1)
        map_figure.gca().add_artist(c)

    else:
        clv3_center = clv3_radius = None
    return clv3_center, clv3_radius


def compute_circle_signal(positions, center, radius, signal_values):
    X = positions[:,0]
    Y = positions[:,1]
    projected_positions = dict(zip(range(len(positions)),np.transpose([X,Y,np.zeros_like(X)])))

    circle_thetas = np.linspace(-180,180,361)
    circle_x = center[0] + radius*np.cos(np.pi*circle_thetas/180.)
    circle_y = center[1] + radius*np.sin(np.pi*circle_thetas/180.)
    circle_z = np.zeros_like(circle_x)
            
    cell_radius=5.0
    density_k = 0.15
            
    circle_potential = np.array([nuclei_density_function(dict([(p,projected_positions[p])]),cell_radius=cell_radius,k=density_k)(circle_x,circle_y,circle_z) for p in xrange(len(positions))])
    circle_potential = np.transpose(circle_potential)
    circle_density = np.sum(circle_potential,axis=1)
    circle_membership = circle_potential/circle_density[...,np.newaxis]

    circle_signal = np.sum(circle_membership*signal_values[np.newaxis,:],axis=1)

    return circle_signal, circle_thetas

def aligned_circle_signal(circle_signal, circle_thetas):
    theta_min = circle_thetas[np.argmin(circle_signal)]

    aligned_thetas = ((circle_thetas-theta_min+180)%360 - 180)
    aligned_signal = circle_signal

    return aligned_signal, aligned_thetas
    

def circle_primordia_angles(circle_signal, circle_thetas, primordia_ranks=[-3,-2,-1,0,1,2,3,5], aligned=False):
    golden_angle = (2.*np.pi)/((np.sqrt(5)+1)/2.+1)
    golden_angle = 180.*golden_angle/np.pi 
    
    theta_min = circle_thetas[np.argmin(circle_signal)]
    max_points, min_points = local_extrema(circle_signal,abscissa=circle_thetas)

    primordia_angles = {}
    
    for primordium in primordia_ranks:
        primordium_theta = (theta_min + primordium*golden_angle + 180)%360 - 180
    
        if primordium > 2:
            extremum_points = max_points
        elif primordium > 0:
            extremum_points = np.concatenate([min_points,max_points])
        else:
            extremum_points = min_points
        extremum_match = vq(np.array([primordium_theta]),extremum_points[:,0])
        extremum_theta = extremum_points[:,0][extremum_match[0][0]]
        extremum_error = (extremum_theta-primordium_theta + 180)%360 - 180
        print "P",primordium," : ",extremum_theta,"(",primordium_theta,") : ",np.abs(extremum_error)
        
        if np.abs(extremum_error)<np.abs(golden_angle/4.):
                primordia_angles[primordium] = extremum_theta

    return primordia_angles



