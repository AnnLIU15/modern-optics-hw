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

def plot_sd(is_save: bool = True,
            is_show: bool = True,
            base_dir: Union[int,str] = 0,
             ) -> None:
    r'''plot the spectral power density value

    Args:
        csv_path (Union[str,List[str]]): csv path(s)
        is_save (bool, optional): flag of save figure. Defaults to True.
        is_show (bool, optional): flag of show figure. Defaults to True.
    '''
    

    if isinstance(base_dir,str):
        base_dir = base_dir
    else:
        raise TypeError(f'Unspport base dir type {type(base_dir)}')
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    fig, axes = plt.subplots(1, 1, figsize=(8,8), tight_layout=True)
    for type_xyz in range(2):
        xyz_str = 'xyz cie2006' if type_xyz else 'xyz cie1931'
        (fig_tmp,_), _, _, line_xy = get_background(type_xyz=type_xyz)
        plt.close(fig_tmp)
        line_xy_e = np.concatenate([line_xy[:,:],   # line_xy_expended_data
                                    line_xy[0,:][np.newaxis,:]],
                                    axis=0)
        
        axes.plot(line_xy_e[:,0],line_xy_e[:,1],'--',
                  color='#333333' if type_xyz else '#FF0000',
                  label=f'{xyz_str}(area: {np.round(polygon_area(line_xy_e),4)})')
    
    axes.set_title(f'Chromatic Diagram Compare(cie1931 vs cie2006)')
    axes.legend(loc=1,frameon=False)# axes.legend(loc='upper right')
    axes.set_xlabel('x'), axes.set_ylabel('y')
    axes.grid(visible=True)
    axes.set_xlim([-.1,.9]), axes.set_ylim([-.1,.9])
    if is_save:
        plt.savefig(f'{base_dir}/cmp-sd.pdf', format = 'pdf',
                bbox_inches='tight',pad_inches = 0,transparent = True)
        plt.savefig(f'{base_dir}/cmp-sd.svg', format = 'svg',
                    bbox_inches='tight',pad_inches = 0,transparent = True)
        plt.savefig(f'{base_dir}/cmp-sd.png', format = 'png', dpi=300,
                    bbox_inches='tight',pad_inches = 0,transparent = True)
    if is_show:
        plt.show()
    plt.close('all')
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--is_save',action='store_false')
    parser.add_argument('--is_show',action='store_true')
    parser.add_argument('--base_dir',default='outputs/')
    args = parser.parse_args()
    plot_sd(is_save = args.is_save,
            is_show = args.is_show,
            base_dir = args.base_dir,
            )