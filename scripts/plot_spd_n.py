import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import Union, List
import os
import sys
from pathlib import Path
import argparse
base_path = str(Path(__file__).resolve().parent.parent)
sys.path.append(base_path)
from utils import get_spd,spd_background

def plot_spd(csv_path: Union[str,List[str]],
             is_save: bool = True,
             is_show: bool = True,
             ) -> None:
    r'''plot the spectral power density value

    Args:
        csv_path (Union[str,List[str]]): csv path(s)
        is_save (bool, optional): flag of save figure. Defaults to True.
        is_show (bool, optional): flag of show figure. Defaults to True.
    '''
    if isinstance(csv_path,str):
        csv_path = [csv_path]
    for cur_file in csv_path:
        spd_data,file_str,wavelengths = get_spd(cur_file,if_sep=True)
        base_dir = ['outputs'] + cur_file.replace('\\','/').split('/')[1:-1]
        base_dir = '/'.join(base_dir) + '/'
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        # print('data/psu_llab/CQS-1-NM.csv'[:'data/psu_llab/CQS-1-NM.csv'.index(file_str)])
        for idx in range(spd_data.shape[-1]):
            spd_data[:,idx] /= np.max(spd_data[:,idx])
        spd_data_sum = spd_data.sum(axis=1)
        limits: np.ndarray = np.array([380, 780])

        fig, axes = plt.subplots(2, 1, figsize=(8, 4), tight_layout=True)
        for idx in range(2):
            plt.figure(fig)
            cur_xyz_name = 'CIE 2006-XYZ' if idx else 'CIE 1931-XYZ'
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
            axes[idx].set_title(cur_xyz_name)
            axes[idx].spines['top'].set_visible(False)
            axes[idx].spines['left'].set_visible(False)
            axes[idx].spines['right'].set_visible(False)
            axes[idx].get_yaxis().set_visible(False)
            fig_idx, ax = plt.subplots(1, 1, figsize=(8, 4), tight_layout=True)
            polygon_1  = patches.Polygon(
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
            ax.add_patch(polygon_1)
            ax.bar(
                x=wave_length - padding,
                height=1,
                width=sep + padding,
                color=RGB_back,
                align="edge",
                clip_path=polygon_1,
                zorder=-140
            )
            ax.set_xlabel(r'$\lambda$/nm')
            ax.set_ylabel('Intensity')
            ax.set_title(f'Spectral Power Distribution {file_str} '
                          + f'({cur_xyz_name})')
            ax.spines['top'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.get_yaxis().set_visible(False)
            if is_save:

                plt.savefig(f'{base_dir}/{file_str}-{cur_xyz_name[4:8]}-spd-n.pdf',
                            format = 'pdf', bbox_inches='tight',pad_inches = 0,transparent = True)
                plt.savefig(f'{base_dir}/{file_str}-{cur_xyz_name[4:8]}-spd-n.svg', 
                            format = 'svg', bbox_inches='tight',pad_inches = 0,transparent = True)
                plt.savefig(f'{base_dir}/{file_str}-{cur_xyz_name[4:8]}-spd-n.png', 
                            format = 'png', dpi=300, bbox_inches='tight',pad_inches = 0,transparent = True)
        plt.figure(fig)
        plt.suptitle(f'Spectral Power Distribution {file_str}')
        if is_save:
            plt.savefig(f'{base_dir}/{file_str}-spd-n.pdf', format = 'pdf',
                    bbox_inches='tight',pad_inches = 0,transparent = True)
            plt.savefig(f'{base_dir}/{file_str}-spd-n.svg', format = 'svg',
                        bbox_inches='tight',pad_inches = 0,transparent = True)
            plt.savefig(f'{base_dir}/{file_str}-spd-n.png', format = 'png', dpi=300,
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
    
    plot_spd(csv_path = args.files,
            is_save = args.is_save,
            is_show = args.is_show,
            )