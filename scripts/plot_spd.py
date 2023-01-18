import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import Union, List
import os
import sys
from pathlib import Path
base_path = str(Path(__file__).resolve().parent.parent)
sys.path.append(base_path)
from utils import get_spd,spd_background
import copy

def plot_spd(csv_path: Union[str,List[str]],
             if_save: bool = True,
             if_show: bool = True,
             ) -> None:
    r'''plot the spectral power density value

    Args:
        csv_path (Union[str,List[str]]): csv path(s)
        if_save (bool, optional): flag of save figure. Defaults to True.
        if_show (bool, optional): flag of show figure. Defaults to True.
    '''
    if isinstance(csv_path,str):
        csv_path = [csv_path]
    for cur_file in csv_path:
        spd_data,file_str,wavelengths = get_spd(cur_file,)
        ['outputs'] + cur_file.replace('\\','/').split('/')[1:-1]
        base_dir = ['outputs'] + cur_file.replace('\\','/').split('/')[1:-1]
        base_dir = '/'.join(base_dir) + '/'
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        # print('data/psu_llab/CQS-1-NM.csv'[:'data/psu_llab/CQS-1-NM.csv'.index(file_str)])
        spd_data_sum = spd_data.sum(axis=1)
        limits: np.ndarray = np.array([380, 780])

        fig, axes = plt.subplots(2, 1, figsize=(8, 4), tight_layout=True)
        for idx in range(2):
            plt.figure(fig)
            cur_xyz_name = 'xyz cie2006' if idx else 'xyz cie1931'
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
            if if_save:

                plt.savefig(f'{base_dir}/{file_str}-spd-{cur_xyz_name}.pdf', format = 'pdf',
                        bbox_inches='tight',pad_inches = 0,transparent = True)
                plt.savefig(f'{base_dir}/{file_str}-spd-{cur_xyz_name}.svg', format = 'svg',
                            bbox_inches='tight',pad_inches = 0,transparent = True)
                plt.savefig(f'{base_dir}/{file_str}-spd-{cur_xyz_name}.png', format = 'png', dpi=300,
                            bbox_inches='tight',pad_inches = 0,transparent = True)
        plt.figure(fig)
        plt.suptitle(f'Spectral Power Distribution {file_str}')
        if if_save:
            plt.savefig(f'{base_dir}/{file_str}-spd.pdf', format = 'pdf',
                    bbox_inches='tight',pad_inches = 0,transparent = True)
            plt.savefig(f'{base_dir}/{file_str}-spd.svg', format = 'svg',
                        bbox_inches='tight',pad_inches = 0,transparent = True)
            plt.savefig(f'{base_dir}/{file_str}-spd.png', format = 'png', dpi=300,
                        bbox_inches='tight',pad_inches = 0,transparent = True)
        if if_show:
            plt.show()
        plt.close('all')


def unittest():
    plot_spd(['data/psu_llab/CQS-1-NM.csv'],)


if __name__ == '__main__':
    unittest()