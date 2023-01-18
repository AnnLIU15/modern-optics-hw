import numpy as np
import matplotlib.pyplot as plt
from typing import List
import os
import sys
from pathlib import Path
base_path = str(Path(__file__).resolve().parent.parent)
sys.path.append(base_path)
from utils import read_data_from_csv


def get_tristimulus(csv_path: str,
                    str_list: List[str],
                    is_save: bool = True,
                    is_show: bool = True,
                    base_dir: str = 'outputs/Tristimulus') -> None:
    r'''get the tristimulus value

    Args:
        csv_path (str): csv path
        str_list (List[str]): xyz rgb
        is_save (bool, optional): flag of save figure. Defaults to True.
        is_show (bool, optional): flag of show figure. Defaults to True.
        base_dir (str, optional): based save dir. Defaults to './outputs/Tristimulus'.
    '''
    
    data = read_data_from_csv(csv_path,if_limits=False)
    origin_data = data[0][0]
    rgb_list = ['r','g','b']
    fig = plt.figure(figsize=(12,6))
    for idx in range(1,4,1):
        plt.plot(origin_data[:,0],origin_data[:,idx],rgb_list[idx-1],
             label=r'$\overline{%s}(\lambda)$'%(str_list[idx-1]))
    plt.xlabel(r'$\lambda$/nm')
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend(frameon = False)
    title_type = ''.join(str_list)
    plt.title(f'CIE 1931 {title_type.upper()} Tristimulus Values')
    plt.xlim([origin_data[0,0],origin_data[-1,0]])
    if is_save:
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        plt.savefig(f'{base_dir}/{title_type}.pdf', format = 'pdf',
                bbox_inches='tight',pad_inches = 0,transparent = True)
        plt.savefig(f'{base_dir}/{title_type}.svg', format = 'svg',
                    bbox_inches='tight',pad_inches = 0,transparent = True)
        plt.savefig(f'{base_dir}/{title_type}.png', format = 'png', dpi=300,
                            bbox_inches='tight',pad_inches = 0,transparent = True)
    if is_show:
        plt.show()
    else:
        plt.close()


def unittest():
    get_tristimulus('data/xyz_tri.csv',['x','y','z'],is_show = False)
    get_tristimulus('data/rgb_tri.csv',['r','g','b'],is_show = False)



if __name__ == '__main__':
    unittest()