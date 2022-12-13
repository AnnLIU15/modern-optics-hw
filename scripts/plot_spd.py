import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import os
import sys
from pathlib import Path
base_path = str(Path(__file__).resolve().parent.parent)
sys.path.append(base_path)
from utils import read_data_from_csv, wavelength_to_rgba


def get_spd(csv_path: str,
            limits: np.ndarray = np.array([380, 780]),
            if_save: bool = True,
            if_show: bool = True,
            if_sep: bool = True,
            sep: float = 0.5,
            base_dir: str = 'outputs/SPD') -> None:
    r'''plot the spectral power density value

    Args:
        csv_path (str): csv path
        limits (np.ndarray, optional): the wavelength . Defaults to np.array([380,780]).
        if_save (bool, optional): flag of save figure. Defaults to True.
        if_show (bool, optional): flag of show figure. Defaults to True.
        sep (float, optional): step of wave. Defaults to 0.5.
        base_dir (str, optional): based save dir. Defaults to './outputs/Tristimulus'.
    '''
    wl = np.arange(limits[0],limits[1]+1,sep)
    colorlist = wavelength_to_rgba(wl,0.8)
    
    data_list = read_data_from_csv(csv_path,limits = limits, if_limits=True,if_sep=if_sep)
    for data, name in data_list:
        wl = np.arange(limits[0],limits[1]+1,sep)
        colorlist = wavelength_to_rgba(wl,0.8)
        # spectralmap = LinearSegmentedColormap.from_list("spectrum", colorlist)
        
        wavelengths = data[:,0]
        spectrum = data[:,2]
        fig, axes = plt.subplots(1, 1, figsize=(8,4), tight_layout=True)
        plt.plot(wavelengths, spectrum, color='k')
        polygon = patches.Polygon(
            np.vstack(
                [
                    (limits[0], 0),
                    np.hstack((wavelengths[:,np.newaxis],spectrum[:,np.newaxis])),
                    (limits[1], 0),
                ]
            ),
            facecolor="none",
            edgecolor="none",
            zorder=-140
        )
        axes.add_patch(polygon)
        padding = 0.2
        axes.bar(
            x= wl- padding,
            height=max(spectrum),
            width= sep + padding,
            color=colorlist[:,:3],
            align="edge",
            clip_path=polygon,
            zorder=-140
        )
        
        plt.xlabel(r'$\lambda$/nm')
        plt.ylabel('Intensity')
        # ax = plt.gca()
        axes.spines['top'].set_visible(False)
        axes.spines['left'].set_visible(False)
        axes.spines['right'].set_visible(False)
        axes.get_yaxis().set_visible(False)
        # axes.legend(frameon = False)
        plt.title(f'{name.upper()} SPD (380,780)nm')
        plt.xlim(limits)
        if if_save:
            if not os.path.exists(base_dir):
                os.makedirs(base_dir)
            plt.savefig(f'{base_dir}/{name}.pdf', format = 'pdf',
                    bbox_inches='tight',pad_inches = 0,transparent = True)
            plt.savefig(f'{base_dir}/{name}.svg', format = 'svg',
                        bbox_inches='tight',pad_inches = 0,transparent = True)
        if not if_show:
            plt.close('all')
    if if_show:
        plt.show()
    else:
        plt.close('all')


def unittest():
    get_spd(['data\CIE\CIE_illum_D50.csv','data\CIE\CIE_cc_1931_2deg.csv'],)


if __name__ == '__main__':
    unittest()