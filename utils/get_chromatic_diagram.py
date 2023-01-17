import numpy as np
from typing import Tuple, Union
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.transform_matrix import CAT_CAT02,XYZ2SRGB,spow
from utils.read_data import read_data_from_csv
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from utils.get_spd import get_spd
def get_background(default_D65_path: str =
                   'data/CIE_illum_single/CIE_std_illum_D65.csv',
                   default_xyz1931_path: str =
                   'data/xyz_tri.csv',
                   default_xyz2006_path: str =
                   'data/xyz_tri2006.csv',
                   type_xyz: int = 0,  # 0 -> 1931, 1 -> 2006,
                   samples:int=256,
                   ) -> Tuple[Tuple[plt.Figure,plt.Axes],np.ndarray,np.ndarray]:
    default_data = read_data_from_csv(
        [default_D65_path, default_xyz1931_path, default_xyz2006_path])
    D65_data, xyz1931, xyz2006 = default_data[:]  # tuple
    D65_data, xyz1931, xyz2006 = D65_data[0], xyz1931[0], xyz2006[0]  # data
    xyz_tri = xyz2006 if type_xyz else xyz1931
    wave_length, XYZ = xyz_tri[:, 0], xyz_tri[:, 1:]

    xy_data = XYZ[:,:2]/(np.sum(XYZ,axis=1)[:,np.newaxis] + 1e-10)
    if type_xyz == 1:
        xy_data[:10,0] = xy_data[10,0] + 5e-10
        xy_data[:10,1] = xy_data[10,1] - 3.3e-10
    xy_data_1 = np.concatenate([xy_data[:,:],
                                xy_data[0,:][np.newaxis,:]],
                                 axis=0)

    XYZ_D65 = D65_data[:, 1].T@xyz_tri[:, 1:]
    XYZ_D65 = XYZ_D65/XYZ_D65[1]
    xy_D65 = XYZ_D65[:2]/np.sum(XYZ_D65)
    # RGB_w = CAT_CAT02 @ XYZ_D65[:, np.newaxis,]
    # RGB_wr = CAT_CAT02 @ XYZ_D65[:, np.newaxis,]
    # with np.errstate(divide="ignore", invalid="ignore"):
    #     D = np.nan_to_num(RGB_wr / RGB_w, nan=0, posinf=0, neginf=0)
    # D = np.diag(D.flatten())
    # # Chromatic adaptation matrix :math:`M_{cat}`.
    # M_CAT = np.round(np.linalg.inv(CAT_CAT02) @ D @ CAT_CAT02,10)
    # XYZ_change = XYZ@M_CAT.T
    
    ii, jj = np.meshgrid(
            np.linspace(0, 1, samples), np.linspace(1, 0, samples)
        )
    ij = np.concatenate((ii[...,np.newaxis],jj[...,np.newaxis]),axis=-1)
    xyY = np.concatenate((ij,np.ones_like(ii)[...,np.newaxis]),axis=-1)
    x,y,Y = xyY[...,0],xyY[...,1],xyY[...,2]
    XYZ_cg = np.zeros_like(xyY)
    m_XYZ = ~(y == 0)
    Y_y = Y[m_XYZ] / y[m_XYZ]
    XYZ_cg[m_XYZ] = np.vstack(
            [x[m_XYZ] * Y_y, Y[m_XYZ], (1 - x[m_XYZ] - y[m_XYZ]) * Y_y]
        ).T
    RGB_cg = np.einsum("...ij,...j->...i", XYZ2SRGB, XYZ_cg)
    RGB_cg = np.where(RGB_cg>0.0031308,1.055*spow(RGB_cg,(1/2.4))-0.055,12.92*RGB_cg)
    with np.errstate(divide="ignore", invalid="ignore"):
        c = np.nan_to_num(1 / RGB_cg.max(axis = -1)[..., None], nan=0, posinf=0, neginf=0)
    factor = 1
    RGB_cg = RGB_cg * c * factor
    RGB_cg = np.clip(RGB_cg,0,factor)
    fig, axes = plt.subplots(1, 1, figsize=(8,8), tight_layout=True)
    polygon = patches.Polygon(
        xy_data[:,:2],
        facecolor="none",
        edgecolor="none",
        zorder=-140
    )
    axes.add_patch(polygon)
    # show RGB CG image
    axes.imshow(
                RGB_cg,
                interpolation="bicubic",
                extent=(0, 1, 0, 1),
                clip_path=polygon,
                alpha=1,
                zorder=-140,
            )
    # image.set_clip_path(polygon)
    axes.plot(xy_data_1[:,0],xy_data_1[:,1],color='#333333')


    labels = np.array([390, 460, 470, 480, 490, 500, 510,
                    520, 540, 560, 580, 600, 620, 700])

    for label in labels:
        data_dict = dict(zip(wave_length,xy_data_1))
        ij_l = data_dict.get(label)
        index = np.argwhere(wave_length==label)[0,0]
        left = wave_length[index - 1] if index >= 0 else wave_length[index]
        right = (
                wave_length[index] if index < len(wave_length) else wave_length[-1]
                )
        dx = data_dict[right][0] - data_dict[left][0]
        dy = data_dict[right][1] - data_dict[left][1]
        direction = np.array([-dy, dx])
        normalized_d = direction/np.linalg.norm(direction)
        tmp_ij_l = ij_l - [1/3,1/3]
        tmp_ij_l = tmp_ij_l/np.linalg.norm(tmp_ij_l)
        true_d = np.array([-dy, dx]) \
                if np.dot(normalized_d,tmp_ij_l) > 0 \
                else np.array([dy, -dx])
        true_d = (true_d/np.linalg.norm(true_d)) / 30
        i , j = ij_l
        axes.plot(
                (i, i + true_d[0] * 0.75),
                (j, j + true_d[1] * 0.75),
                color='#333333', alpha=1, zorder= -120,
            )
        axes.plot(
                i, j, "o", color='#333333',markersize=4,
                alpha=1, zorder= -120,)
        axes.text(
                i + true_d[0], j + true_d[1],
                label, clip_on=True,
                ha="left" if true_d[0] >= 0 else "right",
                va="center", fontdict={"size": "small"},
                zorder=-100,
            )
        axes.set_xlim([-.1,.9]),axes.set_ylim([-.1,.9])
        axes.grid(visible=True)
    axes.set_xlim([-.1,.9]),axes.set_ylim([-.1,.9])
    # plt.xlim([-0.1,0.9]),plt.ylim([-0.1,0.9])
    # plt.scatter(xy[:,0],xy[:,1])
    # new_xy = np.vstack((xy,xy[0,:][None,:]))

    # axes.plot(new_xy[..., 0], new_xy[..., 1])
    # plt.scatter(0.31270, 0.32900) # D65
    axes.scatter(xy_D65[0],xy_D65[1],color='#333333',
                 label=f'D65-White {np.round(xy_D65,4)}')
    # axes.text(
    #             xy_D65[0],xy_D65[1],
    #             xy_D65, clip_on=True,
    #             ha="left" if true_d[0] >= 0 else "right",
    #             va="center", fontdict={"size": "small"},
    #             zorder=-100,
    #         )
    
    return (fig,axes), wave_length, XYZ


def unittest():
    type_xyz = 0
    (fig,axes), wave_length, XYZ = get_background(type_xyz=type_xyz)
    spd_data,file_str,wavelengths = get_spd('data/psu_llab/CQS-1-NM.csv',)
    XYZ_SPD = spd_data.T@XYZ
    idx_sum = XYZ_SPD.sum(axis=1)
    xy = np.zeros((3,2))
    for idx in range(3):
        xy[idx,:] = [XYZ_SPD[idx,:2]]/idx_sum[idx]
    new_xy = np.vstack((xy,xy[0,:][None,:]))
    axes.scatter(xy[:,0],xy[:,1],color='#333333')
    axes.plot(new_xy[..., 0], new_xy[..., 1],color='#333333',label=file_str)
    NTSC = np.array(
        [
            [0.630, 0.340],
            [0.310, 0.595],
            [0.155, 0.070], # white point (CIE illuminant D65)	0.3127	0.3290
        ]
    )   # https://en.wikipedia.org/wiki/NTSC
    new_NTSC = np.vstack((NTSC,NTSC[0,:][None,:]))
    axes.scatter(NTSC[:,0],NTSC[:,1],color='#0000FF')
    axes.plot(new_NTSC[..., 0], new_NTSC[..., 1],color='#0000FF',label='NTSC')
    axes.legend(loc=1)# axes.legend(loc='upper right')
    axes.set_title('xyz cie2006' if type_xyz else 'xyz cie1931')
    plt.show()
    
if __name__ == '__main__':
    unittest()
