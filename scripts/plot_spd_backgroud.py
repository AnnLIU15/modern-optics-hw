import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sys
from pathlib import Path
import argparse
base_path = str(Path(__file__).resolve().parent.parent)
sys.path.append(base_path)
from utils import spd_background






if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--is_save',action='store_false')
    parser.add_argument('--is_show',action='store_true')
    parser.add_argument('--base_dir',default='outputs')
    args = parser.parse_args()
    limits: np.ndarray = np.array([380, 780])
    for idx in range(2):
        fig, axes = plt.subplots(1, 1, figsize=(8, 4), tight_layout=True)
        cur_xyz_name = 'CIE 2006-XYZ' if idx else 'CIE 1931-XYZ'
        RGB_back, wave_length = spd_background(type_xyz=idx)
        
        sep = wave_length[1]-wave_length[0]
        padding = 0.1
        axes.bar(
            x=wave_length - padding,
            height=1,
            width=sep + padding,
            color=RGB_back,
            align="edge",
            zorder=-140
        )
        axes.set_xlabel(r'$\lambda$/nm')
        axes.set_ylabel('Intensity')
        axes.set_title(cur_xyz_name)
        axes.spines['top'].set_visible(False)
        axes.spines['left'].set_visible(False)
        axes.spines['right'].set_visible(False)
        axes.get_yaxis().set_visible(False)
        
        if args.is_save:
            

            plt.savefig(f'{args.base_dir}/{cur_xyz_name}-spd.pdf',
                            format = 'pdf', bbox_inches='tight',pad_inches = 0,transparent = True)
            plt.savefig(f'{args.base_dir}/{cur_xyz_name}-spd.svg', 
                            format = 'svg', bbox_inches='tight',pad_inches = 0,transparent = True)
            plt.savefig(f'{args.base_dir}/{cur_xyz_name}-spd.png', 
                            format = 'png', dpi=300, bbox_inches='tight',pad_inches = 0,transparent = True)
        if args.is_show:
            plt.show()
    plt.close('all')
        