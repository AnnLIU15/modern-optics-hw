import numpy as np
# http://www.brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html

# matrix_XYZ_to_RGB = np.array(
#     [
#         [3.24062548, -1.53720797, -0.49862860],
#         [-0.96893071, 1.87575606, 0.04151752],
#         [0.05571012, -0.20402105, 1.05699594],
#     ]
# )

# matrix_RGB_to_XYZ = np.array(
#     [
#         [0.41240000, 0.35760000, 0.18050000],
#         [0.21260000, 0.71520000, 0.07220000],
#         [0.01930000, 0.11920000, 0.95050000],
#     ])

matrix_XYZ_to_RGB = np.array(
    [
        [2.7688, 1.7517, 1.1301],
        [1, 4.5906, 0.0601],
        [0., 0.0565, 5.5942],
    ]
)
matrix_RGB_to_XYZ = np.array(
    [
        [0.4185, -0.1587, -0.0828],
        [-0.0912, 0.2524, 0.0157],
        [0.0009, -0.0025, 0.1786],
    ])



print(np.round(matrix_XYZ_to_RGB@matrix_RGB_to_XYZ,8))