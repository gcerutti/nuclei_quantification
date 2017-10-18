import matplotlib as mpl
from matplotlib import cm
import numpy as np

from openalea.oalab.colormap.colormap_def import load_colormaps

primordia_colors = {}
primordia_colors[-3] = "#333333"
primordia_colors[-2] = "#0ce838"
primordia_colors[-1] = "#0065ff"
primordia_colors[0] = "#64bca4"
primordia_colors[1] = "#e30d00"
primordia_colors[2] = "#ffa200"
primordia_colors[3] = "#cccccc"
primordia_colors[4] = "#dddddd"
primordia_colors[5] = "#eeeeee"

clv3_color = "#c94389"

cmaps = {}
for cmap_name in ['1Flashy_green','1Flashy_purple','1Flashy_orange','1Flashy_turquoise','geo_jet']:
    cmap = load_colormaps()[cmap_name]

    color_dict = dict(red=[],green=[],blue=[])
    for p in np.sort(cmap._color_points.keys()):
        for k,c in enumerate(['red','green','blue']):
            color_dict[c] += [(p,cmap._color_points[p][k],cmap._color_points[p][k])]
    for c in ['red','green','blue']:
        color_dict[c] = tuple(color_dict[c])
    cm.register_cmap(cmap_name,mpl.colors.LinearSegmentedColormap(cmap.name, color_dict))

    color_dict = dict(red=[],green=[],blue=[])
    for p in np.sort(cmap._color_points.keys()):
        for k,c in enumerate(['red','green','blue']):
            color_dict[c] = [(1-p,cmap._color_points[p][k],cmap._color_points[p][k])] + color_dict[c]
    for c in ['red','green','blue']:
        color_dict[c] = tuple(color_dict[c])
    cm.register_cmap(cmap_name+"_r",mpl.colors.LinearSegmentedColormap(cmap.name+"_r", color_dict))

signal_ranges= {}
signal_ranges['DIIV'] = (1000,8000)
signal_ranges['qDII'] = (0,1.0)
signal_ranges['Auxin'] = (0,1.0)
signal_ranges['DR5'] = (0,25000)
signal_ranges['AHP6'] = (0,10000)
signal_ranges['CLV3'] = (0,20000)
signal_ranges['TagBFP'] = (0,15000)
signal_ranges['gaussian_curvature'] = (-0.001,0.001)
signal_ranges['nuclei_distance'] = (0,15)
signal_ranges['surface_distance'] = (0,100)
signal_ranges['sam_id'] = (0,30)
signal_ranges['next_relative_surfacic_growth'] = (0.9,1.3)

signal_lut_ranges= {}
signal_lut_ranges['CLV3'] = (0,10000)
signal_lut_ranges['DIIV'] = (500,6000)
signal_lut_ranges['qDII'] = (0,0.3)
signal_lut_ranges['Auxin'] = (0.7,1.)
signal_lut_ranges['DR5'] = (0,12000)
signal_lut_ranges['AHP6'] = (0,8000)
signal_lut_ranges['TagBFP'] = (0,15000)
signal_lut_ranges['gaussian_curvature'] = (-0.001,0.001)
signal_lut_ranges['nuclei_distance'] = (0,15)
signal_lut_ranges['surface_distance'] = (0,100)
signal_lut_ranges['sam_id'] = (0,30)
signal_lut_ranges['next_relative_surfacic_growth'] = (0.9,1.3)

signal_colormaps = {}
signal_colormaps['CLV3'] = '1Flashy_purple'
signal_colormaps['DIIV'] = '1Flashy_green'
signal_colormaps['qDII'] = '1Flashy_green'
signal_colormaps['Auxin'] = '1Flashy_green_r'
signal_colormaps['DR5'] = '1Flashy_orange'
signal_colormaps['AHP6'] = '1Flashy_turquoise'
signal_colormaps['TagBFP'] = 'gray'
signal_colormaps['gaussian_curvature'] = 'RdBu_r'
signal_colormaps['nuclei_distance'] = 'geo_jet'
signal_colormaps['surface_distance'] = 'geo_jet'
signal_colormaps['sam_id'] = 'Blues'
signal_colormaps['next_relative_surfacic_growth'] = 'jet'

contour_ranges = {}
contour_ranges['Normalized_DIIV'] = (0.25,0.45)
# contour_ranges['qDII'] = (0.3,0.5)
contour_ranges['qDII'] = (-0.05,0.15)
contour_ranges['Auxin'] = (0.45,0.65)
contour_ranges['Normalized_DR5'] = (0.75,1.25)
contour_ranges['DR5'] = (4000,10000)
contour_ranges['gaussian_curvature'] = (-0.0005,-0.00005)
contour_ranges['next_relative_surfacic_growth'] = (1.09,1.19)

contour_colormaps = {}
contour_colormaps['Normalized_DIIV'] = 'Greens'
contour_colormaps['qDII'] = 'winter_r'
contour_colormaps['Auxin'] = 'spring_r'
contour_colormaps['Normalized_DR5'] = 'Oranges_r'
contour_colormaps['DR5'] = '1Flashy_orange'
contour_colormaps['gaussian_curvature'] = 'winter'
contour_colormaps['next_relative_surfacic_growth'] = 'viridis'

