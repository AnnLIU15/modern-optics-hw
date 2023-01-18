import numpy as np
'''
matrix from colour
colour/models/rgb/rgb_colourspace.py
https://github.com/colour-science/colour/blob/develop/colour/models/rgb/rgb_colourspace.py
'''
# 
# 

SRGB2XYZ = np.array(
    [
        [0.41240000, 0.35760000, 0.18050000],
        [0.21260000, 0.71520000, 0.07220000],
        [0.01930000, 0.11920000, 0.95050000],
    ])



XYZ2SRGB = np.array(
    [
        [3.24062548, -1.53720797, -0.49862860],
        [-0.96893071, 1.87575606, 0.04151752],
        [0.05571012, -0.20402105, 1.05699594],
    ]
    )
''' matrix from colour
colour/adaptation/datasets/cat.py
https://github.com/colour-science/colour/blob/develop/colour/adaptation/datasets/cat.py
'''

CAT_CAT02 = np.array(
    [
        [0.7328, 0.4296, -0.1624],
        [-0.7036, 1.6975, 0.0061],
        [0.0030, 0.0136, 0.9834],
    ]
)
# colour


NTSC = np.array(
    [
        [0.630, 0.340],
        [0.310, 0.595],
        [0.155, 0.070], # white point (CIE illuminant D65)	0.3127	0.3290
    ]
)   # https://en.wikipedia.org/wiki/NTSC

def spow(data,exp):
    data_p = np.sign(data) * np.abs(data) ** exp
    data_p[np.isnan(data_p)] = 0
    return data_p