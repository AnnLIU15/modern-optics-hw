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
    xyz_str = 'CIE 2006-XYZ' if type_xyz else 'CIE 1931-XYZ'
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
    (fig,axes), wave_length, XYZ, line_xy = get_background(type_xyz=type_xyz,is_plot_white=0)
    spd_data,file_str,wavelengths = get_spd(csv_path,spd_type=0)
    file_length = len(file_str)
    data_len = int(spd_data.shape[-1]/file_length)

    new_NTSC = np.vstack((NTSC,NTSC[0,:][None,:]))
    axes.scatter(NTSC[:,0],NTSC[:,1],color='#9933FF')
    axes.plot(new_NTSC[..., 0], new_NTSC[..., 1],'--',color='#333333',label='NTSC')
    NTSC_AREA = polygon_area(NTSC)
    for idx,file_name in enumerate(file_str):
        cur_spd_data = spd_data[:,idx*data_len:(idx+1)*data_len]
        half_power = None
        blue_wave_length = 1000000
        XYZ_SPD = cur_spd_data.T@XYZ
        idx_sum = XYZ_SPD.sum(axis=1)
        xy = np.zeros((3,2))
        for idx_i in range(3):
            xy[idx_i,:] = [XYZ_SPD[idx_i,:2]]/idx_sum[idx_i]
            pos = np.argmax(cur_spd_data[:,idx_i])
            max_val = np.max(cur_spd_data[:,idx_i])
            if blue_wave_length > wavelengths[pos]:
                blue_wave_length = wavelengths[pos]
                half_power_tmp = np.argwhere(cur_spd_data[:,idx_i]>max_val/(2**0.5)).flatten()
                half_power = wavelengths[[half_power_tmp[0],half_power_tmp[-1]]]
                blue_spd = cur_spd_data[:,idx_i]
        left_move_idx = int(half_power[0] - 380)
        right_move_idx = int(780 - half_power[1])
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

        funcion_list = []
        for idx_l in range(3):
            w = np.polyfit(new_xy[idx_l:idx_l+2,0],new_xy[idx_l:idx_l+2,1],deg = 1)
            funcion_list.append(np.poly1d(w))
            str_rgb = ''
            for idx_p in range(2):
                if new_xy[idx_l+idx_p,0] == min(new_xy[:,0]):
                    str_rgb += 'b'
                elif new_xy[idx_l+idx_p,1] == max(new_xy[:,1]):
                    str_rgb += 'g'
                else:
                    str_rgb += 'r'
            x_w = np.linspace(min(new_xy[idx_l:idx_l+2,0]) - 0.2,
                            max(new_xy[idx_l:idx_l+2,0]) + 0.2)
            y_w = np.poly1d(w)(x_w)
            # axes.plot(x_w,y_w,'--',label=str_rgb)
            
            
        total_move = int(left_move_idx + right_move_idx)
        xy_move_data = np.zeros((total_move,2))
        for idx_move in range(total_move):
            cur_move_spd = np.zeros_like(blue_spd)
            if idx_move < left_move_idx:#left
                move_step = left_move_idx - idx_move
                cur_move_spd[:401-move_step] = blue_spd[move_step:]
                # print(np.sum(cur_move_spd[:-move_step] - blue_spd[move_step:]))
                # equal
            else: # right
                move_step = idx_move - left_move_idx + 1
                cur_move_spd[move_step:] = blue_spd[:-move_step]
            XYZ_SPD = cur_move_spd.T@XYZ
            idx_sum = XYZ_SPD.sum()
            xy_move_data[idx_move,:] = XYZ_SPD[:2]/idx_sum
        axes.scatter(xy_move_data[:,0],xy_move_data[:,1],color='#4B1CE0',marker='o',s=5)
        left_part_xy,right_part_idx = 100,200
        for func in funcion_list:
            print(func)
            x = xy_move_data[left_part_xy:right_part_idx,0]
            y = xy_move_data[left_part_xy:right_part_idx,1]
            y_hat = func(x)
            pos = np.argmin(np.abs(y-y_hat)) + left_part_xy
            
            cur_wave_center = blue_wave_length + 1 + (pos - left_move_idx)
            print(pos,cur_wave_center,xy_move_data[pos,0],xy_move_data[pos,1])
            axes.scatter(xy_move_data[pos,0],xy_move_data[pos,1],color='r',marker='o',s=20)
            # text_x = 0.01 if xy_move_data[pos,0]<0.5 else -0.01
            # text_y = 0.01 if xy_move_data[pos,1]<0.5 else -0.01
            # axes.text(
            #     xy_move_data[pos,0] + text_x, xy_move_data[pos,1] + text_y,
            #     s=f'{cur_wave_center}', clip_on=True,
            #     ha="center", va="center", fontdict={"size": "small"},
            #     zorder=-100,
            # )
            
    axes.set_title(f'Chromatic Diagram with {xyz_str}')
    axes.legend(loc=1,frameon=False)# axes.legend(loc='upper right')
    axes.set_xlabel('x'), axes.set_ylabel('y')
    axes.set_xlim([-.1,.9]), axes.set_ylim([-.1,.9])
    if is_save:
        plt.savefig(f'{base_dir}/{file_name}-4-findP.pdf', format = 'pdf',
                bbox_inches='tight',pad_inches = 0,transparent = True)
        plt.savefig(f'{base_dir}/{file_name}-4-findP.svg', format = 'svg',
                    bbox_inches='tight',pad_inches = 0,transparent = True)
        plt.savefig(f'{base_dir}/{file_name}-4-findP.png', format = 'png', dpi=300,
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
    for type_idx in range(1):   # only cmp 
        plot_sd(csv_path = args.files,
                is_save = args.is_save,
                is_show = args.is_show,
                base_dir = args.base_dir,
                type_xyz = type_idx, 
                )