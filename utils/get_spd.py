import numpy as np
from typing import Tuple, Union
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.transform_matrix import CAT_CAT02,XYZ2SRGB,spow
from utils.read_data import read_data_from_csv


def get_spd(default_spd_path: Union[str,list] = 'data/psu_llab/CQS-1-NM.csv',
            spd_type: int = 0 # 0 -> only return, 1 -> combine
            ) -> Tuple[np.ndarray,str]:
    if type(default_spd_path) == str:
        default_data = read_data_from_csv(
            [default_spd_path])
        spd_data,file_str = default_data[0]
        wave_length, spd_data = spd_data[:,0], spd_data[:,1:]
        spd_data = spd_data/np.max(spd_data)

        spd_data = np.sum(spd_data,axis=1) if spd_type else spd_data
    else:
        default_data = read_data_from_csv(default_spd_path)
        spd_data,file_str = default_data[0]
        wave_length, spd_data = spd_data[:,0], spd_data[:,1:]
        for spd_data_dict in default_data[1:]:
            spd_data = np.concatenate((spd_data,spd_data_dict[0][:,1:]),axis=1)
        spd_data = spd_data/np.max(spd_data)
        spd_data = np.sum(spd_data,axis=1) if spd_type else spd_data
    return spd_data,file_str,wave_length


def spd_background(default_D65_path: str =
                   'data/CIE_illum_single/CIE_std_illum_D65.csv',
                   default_xyz1931_path: str =
                   'data/xyz_tri.csv',
                   default_xyz2006_path: str =
                   'data/xyz_tri2006.csv',
                   type_xyz: int = 0  # 0 -> 1931, 1 -> 2006
                   ) -> Tuple[np.ndarray,np.ndarray]:
    default_data = read_data_from_csv(
        [default_D65_path, default_xyz1931_path, default_xyz2006_path])
    D65_data, xyz1931, xyz2006 = default_data[:]  # tuple
    D65_data, xyz1931, xyz2006 = D65_data[0], xyz1931[0], xyz2006[0]  # data

    xyz_tri = xyz2006 if type_xyz else xyz1931

    XYZ_D65 = D65_data[:, 1].T@xyz_tri[:, 1:]
    XYZ_D65 = XYZ_D65/XYZ_D65[1]
    E_data = np.ones_like(D65_data[:, 1].T)
    XYZ_E = E_data@xyz_tri[:, 1:]
    XYZ_E = XYZ_E/XYZ_E[1]
    ''' NOTE:from xy -> xyY -> XYZ (colour way & jupyter way)
    xy_E_white = np.array([1/3,1/3]) # STD E
    xy_D65_white = np.array([0.31270, 0.32900])
    XYZ_D65 = np.array([xy_D65_white[0]/xy_D65_white[1],
                    1,(1-xy_D65_white[0]-xy_D65_white[1])/xy_D65_white[1]])
    xy_E_white = np.array([1/3,1/3]) # STD E
    # xy -> Y=1 -> xyY -> XYZ
    XYZ_E = np.array([xy_E_white[0]/xy_E_white[1],
                    1,(1-xy_E_white[0]-xy_E_white[1])/xy_E_white[1]])
    '''
    # matrix_chromatic_adaptation_VonKries
    '''
    @incollection{Fairchild2013t,
        title        = {Chromatic {{Adaptation Models}}},
        booktitle    = {Color {{Appearance Models}}},
        author       = {Fairchild, Mark D.},
        year         = 2013,
        edition      = {Third},
        pages        = {4179--4252},
        publisher    = {{Wiley}},
        isbn         = {B00DAYO8E2},
    }'''
    RGB_w = CAT_CAT02 @ XYZ_E[:, np.newaxis,]
    RGB_wr = CAT_CAT02 @ XYZ_D65[:, np.newaxis,]
    with np.errstate(divide="ignore", invalid="ignore"):
        D = np.nan_to_num(RGB_wr / RGB_w, nan=0, posinf=0, neginf=0)
    D = np.diag(D.flatten())
    # Chromatic adaptation matrix :math:`M_{cat}`.
    M_CAT = np.linalg.inv(CAT_CAT02) @ D @ CAT_CAT02
    wave_length, XYZ = xyz_tri[:, 0], xyz_tri[:, 1:]
    XYZ_change = XYZ@M_CAT.T
    RGB = XYZ_change@XYZ2SRGB.T
    factor = 1
    RGB = RGB * factor/RGB.max(axis=None)
    RGB = np.clip(RGB, 0, factor)
    RGB = np.where(RGB > 0.0031308, 1.055*spow(RGB, (1/2.4))-0.055, 12.92*RGB)
    return RGB, wave_length


def unit_test():
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    spd_data,file_str,wavelengths = get_spd('data/psu_llab/CQS-1-NM.csv',)
    spd_data_sum = spd_data.sum(axis=1)
    print(spd_data_sum.shape)
    limits: np.ndarray = np.array([380, 780])
    fig, axes = plt.subplots(2, 1, figsize=(8, 4), tight_layout=True)
    for idx in range(2):
        RGB_back, wave_length = spd_background(type_xyz=idx)
        polygon = patches.Polygon(
            np.vstack(
                [
                    (limits[0], 0),
                    np.hstack((wave_length[:,np.newaxis],spd_data_sum[:,np.newaxis])),
                    (limits[1], 0),
                ]
            ),
            facecolor="none",
            edgecolor="k",
            linewidth=3,
            zorder=-140
        )
        axes[idx].add_patch(polygon)
        sep = wave_length[1]-wave_length[0]
        padding = 0.1
        axes[idx].bar(
            x=wave_length - padding,
            height=1,
            width=sep + padding,
            color=RGB_back,
            align="edge",
            clip_path=polygon,
            zorder=-140
        )
        axes[idx].set_xlabel(r'$\lambda$/nm')
        axes[idx].set_ylabel('Intensity')
        axes[idx].set_title('xyz cie2006' if idx else 'xyz cie1931')
        axes[idx].spines['top'].set_visible(False)
        axes[idx].spines['left'].set_visible(False)
        axes[idx].spines['right'].set_visible(False)
        axes[idx].get_yaxis().set_visible(False)
    plt.suptitle(f'Color Spectrum {file_str}')
    fig.show()
    plt.close(fig)
    # plt.show()


if __name__ == '__main__':
    unit_test()
