import numpy as np
import matplotlib.pyplot as plt
import argparse
from typing import Union, List
import os
import sys
from pathlib import Path
base_path = str(Path(__file__).resolve().parent.parent)
sys.path.append(base_path)
from utils import get_spd,get_background,polygon_area
from utils.transform_matrix import CAT_CAT02,XYZ2SRGB,spow,NTSC

def plot_sd(csv_path: Union[str,List[str]],
            is_save: bool = True,
            is_show: bool = True,
            base_dir: Union[int,str] = 0,
            type_xyz: int = 0, # xyz tri 0 -> cie1931 1 -> cie 2006
             ) -> None:
    r'''plot the spectral power density value

    Args:
        csv_path (Union[str,List[str]]): csv path(s)
        is_save (bool, optional): flag of save figure. Defaults to True.
        is_show (bool, optional): flag of show figure. Defaults to True.
    '''
    xyz_str = 'xyz cie2006' if type_xyz else 'xyz cie1931'
    if isinstance(csv_path,str):
        csv_path = [csv_path]
    if isinstance(base_dir,str):
        base_dir = base_dir
    elif isinstance(base_dir,int):
        assert base_dir<len(csv_path), f'{base_dir} out of range {len(csv_path)}'
        base_dir = ['outputs'] + csv_path[base_dir].replace('\\','/').split('/')[1:-1]
        base_dir = '/'.join(base_dir) + '/'
    else:
        raise TypeError(f'Unspport base dir type {type(base_dir)}')
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    (fig,axes), wave_length, XYZ, line_xy = get_background(type_xyz=type_xyz)
    spd_data,file_str,wavelengths = get_spd(csv_path,spd_type=0)
    file_length = len(file_str)
    data_len = int(spd_data.shape[-1]/file_length)

    new_NTSC = np.vstack((NTSC,NTSC[0,:][None,:]))
    axes.scatter(NTSC[:,0],NTSC[:,1],color='#9933FF')
    axes.plot(new_NTSC[..., 0], new_NTSC[..., 1],'--',color='#333333',label='NTSC')
    NTSC_AREA = polygon_area(NTSC)
    for idx,file_name in enumerate(file_str):
        XYZ_SPD = spd_data[:,idx*data_len:(idx+1)*data_len].T@XYZ
        idx_sum = XYZ_SPD.sum(axis=1)
        xy = np.zeros((3,2))
        for idx_i in range(3):
            xy[idx_i,:] = [XYZ_SPD[idx_i,:2]]/idx_sum[idx_i]
        new_xy = np.vstack((xy,xy[0,:][None,:]))
        for idx_j in range(3):
            if xy[idx_j,0] == min(xy[:,0]):
                str_rgb = 'b'
                color_rgb = '#00CCFF'
            elif xy[idx_j,1] == max(xy[:,1]):
                str_rgb = 'g'
                color_rgb = '#CCFF00'
            else:
                str_rgb = 'r'
                color_rgb = '#FF00CC'
            axes.scatter(xy[idx_j,0],xy[idx_j,1],color=color_rgb,
                         label = f'{file_str[idx]}:{str_rgb} {np.round(xy[idx_j,:],2)}')
        Percent = np.round(polygon_area(xy)/NTSC_AREA*100,2)
        axes.plot(new_xy[..., 0], new_xy[..., 1],color='#333333',
                  label=file_str[idx]+f'(NTSC {Percent}%)')
    
    axes.set_title(f'Chromatic Diagram with {xyz_str}')
    axes.legend(loc=1,frameon=False)# axes.legend(loc='upper right')
    axes.set_xlabel('x'), axes.set_ylabel('y')
    axes.set_xlim([-.1,.9]), axes.set_ylim([-.1,.9])
    if is_save:
        plt.savefig(f'{base_dir}/{file_name}-{xyz_str[-4:]}-sd.pdf', format = 'pdf',
                bbox_inches='tight',pad_inches = 0,transparent = True)
        plt.savefig(f'{base_dir}/{file_name}-{xyz_str[-4:]}-sd.svg', format = 'svg',
                    bbox_inches='tight',pad_inches = 0,transparent = True)
        plt.savefig(f'{base_dir}/{file_name}-{xyz_str[-4:]}-sd.png', format = 'png', dpi=300,
                    bbox_inches='tight',pad_inches = 0,transparent = True)
    if is_show:
        plt.show()
    plt.close('all')
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--files',type=str,nargs='+',default= 'data/psu_llab/CQS-1-NM.csv',
                        help='python xxxx.py --files data/xxx.txt/csv')
    parser.add_argument('--is_save',action='store_false')
    parser.add_argument('--is_show',action='store_true')
    parser.add_argument('--base_dir',default=0)
    args = parser.parse_args()
    for type_idx in range(2):
        plot_sd(csv_path = args.files,
                is_save = args.is_save,
                is_show = args.is_show,
                base_dir = args.base_dir,
                type_xyz = type_idx, 
                )