import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import argparse
from typing import Union, List
import os
import sys
from pathlib import Path
base_path = str(Path(__file__).resolve().parent.parent)
sys.path.append(base_path)
from utils import get_spd,get_background,polygon_area,spd_background,read_data_from_csv
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
        # axes.scatter(xy_move_data[:,0],xy_move_data[:,1],color='#4B1CE0',marker='o',s=5)
        left_part_xy,right_part_idx = 100,200
        data_pos = []
        cur_wave_center = []
        for func in funcion_list:
            x = xy_move_data[left_part_xy:right_part_idx,0]
            y = xy_move_data[left_part_xy:right_part_idx,1]
            y_hat = func(x)
            pos = np.argmin(np.abs(y-y_hat)) + left_part_xy
            data_pos.append(pos)
            cur_wave_center.append(blue_wave_length + 1 + (pos - left_move_idx))

        data_pos = sorted(data_pos)
        cur_wave_center = sorted(cur_wave_center)
        green_pos = xy[:,1].argmax()
        red_pos = xy[:,0].argmax()
        blue_pos = xy[:,0].argmin()
        # xy_rgb = np.vstack((xy[red_pos,:],xy[green_pos,:],xy[blue_pos,:]))
        area = np.zeros(xy_move_data.shape[0])
        blue_max_pos = 0
        for idx_area in range(xy_move_data.shape[0]):
            if blue_max_pos ==0 and idx_area < 90 and xy_move_data[idx_area,1] < xy[blue_pos,1]: # below blue
                p = np.vstack((xy[red_pos,:],xy[green_pos,:],xy[blue_pos,:],xy_move_data[idx_area,:]))
            else:
                blue_max_pos = 1
                if idx_area < data_pos[0]:
                    p = np.vstack((xy[red_pos,:],xy[green_pos,:],xy_move_data[idx_area,:],xy[blue_pos,:],))
                    area[idx_area] = polygon_area(p)
                elif idx_area <= data_pos[1]:
                    p = np.vstack((xy[red_pos,:],xy_move_data[idx_area,:],xy[blue_pos,:],))
                elif idx_area <= 619:
                    p = np.vstack((xy[red_pos,:],xy_move_data[idx_area,:],xy[green_pos,:],xy[blue_pos,:],))
                else:
                    p = np.vstack((xy[red_pos,:],xy_move_data[idx_area,:],xy[green_pos,:],xy[blue_pos,:],))
            area[idx_area] = polygon_area(p)                
        largest_pos = np.argmax(area)
        
        xyY_4 = np.hstack((xy_move_data[largest_pos,:],1))
        XYZ_4 = np.array([[xyY_4[0]/xyY_4[1],1,(1-np.sum(xyY_4[:2]))/xyY_4[1]]])
        RGB_4 = np.einsum("...ij,...j->...i", XYZ2SRGB, XYZ_4)
        RGB_4 = np.where(RGB_4>0.0031308,1.055*spow(RGB_4,(1/2.4))-0.055,12.92*RGB_4)
        with np.errstate(divide="ignore", invalid="ignore"):
            c = np.nan_to_num(1 / RGB_4.max(axis = -1)[..., None], nan=0, posinf=0, neginf=0)
        factor = 1
        RGB_4 = RGB_4 * c * factor
        RGB_4 = np.clip(RGB_4,0,factor)
        RGB_4 = RGB_4.flatten()
        if largest_pos >= left_move_idx:
            largest_wave = blue_wave_length + 1 + (largest_pos - left_move_idx)
        print(f'largest_pos: {largest_pos}, xy: {xy_move_data[largest_pos,:]}')
        print(f'wave: {largest_wave}, colour is {RGB_4}')
        RGB_4 = np.round(RGB_4*255,0)
        print(f'nomalized RGB: {largest_wave}, colour is {RGB_4}')
        wave4_spd = np.zeros_like(blue_spd)
        if largest_pos < left_move_idx:#left
            move_step = left_move_idx - largest_pos
            wave4_spd[:401-move_step] = blue_spd[move_step:]
            # print(np.sum(cur_move_spd[:-move_step] - blue_spd[move_step:]))
            # equal
        else: # right
            move_step = largest_pos - left_move_idx + 1
            wave4_spd[move_step:] = blue_spd[:-move_step]
        wave4_spd = wave4_spd/wave4_spd.max()
        # XYZ_SPD = wave4_spd.T@XYZ
        # idx_sum = XYZ_SPD.sum()
        # aaaa = XYZ_SPD[:2]/idx_sum
        # print(aaaa-xy_move_data[largest_pos,:]) # pos is alright
        RGB_back, wave_length = spd_background(type_xyz=idx)
        fig_idx, ax = plt.subplots(1, 1, figsize=(8, 4), tight_layout=True)
        polygon_1  = patches.Polygon(
            np.vstack(
                [
                    (380, 0),
                    np.hstack((wave_length[:,np.newaxis],wave4_spd[:,np.newaxis])),
                    (780, 0),
                ]
            ),
            facecolor="none",
            edgecolor="k",
            linewidth=3,
            zorder=-140
        )
        ax.add_patch(polygon_1)
        padding = 0.1
        sep = 1
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
        ax.set_title(f'Spectral Power Distribution 4-th color CIE 1931-XYZ')
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_yaxis().set_visible(False)
        if is_save:
            # plt.savefig(f'{base_dir}/{file_str}-{cur_xyz_name[4:8]}-spd.pdf',
            #             format = 'pdf', bbox_inches='tight',pad_inches = 0,transparent = True)
            # plt.savefig(f'{base_dir}/{file_str}-{cur_xyz_name[4:8]}-spd.svg', 
            #             format = 'svg', bbox_inches='tight',pad_inches = 0,transparent = True)
            plt.savefig(f'{base_dir}/{file_name}-spd-4.png', 
                        format = 'png', dpi=300, bbox_inches='tight',pad_inches = 0,transparent = True)
        plt.figure(fig)
        p = np.vstack((xy[red_pos,:],xy[green_pos,:],xy_move_data[largest_pos,:],xy[blue_pos,:],))
        axes.scatter(xy_move_data[largest_pos,0],xy_move_data[largest_pos,1],color='k',
                     label = f'{file_str[idx]}:4-th {np.round(xy_move_data[largest_pos,:],2)}')
        new_p = np.vstack((p,xy[red_pos,:]))
        Percent = np.round(polygon_area(p)/NTSC_AREA*100,2)
        axes.plot(new_p[..., 0], new_p[..., 1],':',color='#333333',
                  label=file_str[idx]+f'(NTSC {Percent}%) with 4-th {largest_wave}')
    axes.set_title(f'Chromatic Diagram with {xyz_str}')
    axes.legend(loc=1,frameon=False)# axes.legend(loc='upper right')
    axes.set_xlabel('x'), axes.set_ylabel('y')
    axes.set_xlim([-.1,.9]), axes.set_ylim([-.1,.9])
    if is_save:
        plt.savefig(f'{base_dir}/{file_name}-4-final.pdf', format = 'pdf',
                bbox_inches='tight',pad_inches = 0,transparent = True)
        plt.savefig(f'{base_dir}/{file_name}-4-final.svg', format = 'svg',
                    bbox_inches='tight',pad_inches = 0,transparent = True)
        plt.savefig(f'{base_dir}/{file_name}-4-final.png', format = 'png', dpi=300,
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