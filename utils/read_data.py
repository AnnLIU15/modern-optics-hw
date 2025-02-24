import numpy as np
from typing import Union, List
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.cubic_Spline import cubic_spline

def read_data_from_csv(relative_paths: Union[List[str],str],
                       limits: np.ndarray = np.array([380,780]), # like colour setting
                       if_limits: bool = True,
                       if_sep: bool = False,
                       ):
    r''' read the Spectral Power Distribution(SPD) data from csv. Clip its wavelength($\lambda$) with limits range 

    Args:
        relative_paths (Union[List[str],str]): the relative path of the data (maybe data list).
        limits (np.ndarray, optional): the wavelength . Defaults to np.array([380,780]).
        if_limits (bool, optional): set limits . Defaults to True.
    Raises:
        TypeError: _description_

    Returns:
        _type_: _description_
    '''
    if isinstance(relative_paths, str):
        relative_paths = [relative_paths]
    elif isinstance(relative_paths, list):
        pass
    else:
        raise TypeError(f'Undefine relative_paths input type: {type(relative_paths)}')
    files_number = len(relative_paths)
    files_info_list = np.zeros(files_number,dtype='object')
    for idx, path in enumerate(relative_paths):
        cur_data = np.loadtxt(path, delimiter=',')
        file_name = path.replace('\\','/').split('/')[-1][:-4].replace(' ','_')
        if if_limits:
            cur_data = set_limits(cur_data, limits, if_sep)
        files_info_list[idx] = (cur_data, file_name)
    return files_info_list


def set_limits(ori_data: np.ndarray,
               limits: np.ndarray = np.array([380,780]), # like colour setting
               if_sep: bool = False,
               tol: float = 1e-5                         # tolerance
               ) ->np.ndarray:
    max_vals = np.max(ori_data, axis = 0)
    min_val = np.min(ori_data[:,0], axis = 0)
    satified_idx = np.logical_and(
        ori_data[:,0] - limits[0] >= -tol,
        limits[1] - ori_data[:,0] >= -tol)
    tmp_data = np.copy(ori_data[satified_idx, :])
    sep = ori_data[1,0] - ori_data[0,0]
    if sep > 1 and if_sep:
        print(f'data sep = {sep}, -> CubicSpline ->  set sep = 1 (current if_sep = True)')
        sep = 1
        begin, end = tmp_data[0,0], tmp_data[-1,0]
        new_wave = np.arange(begin,end+1,sep)
        new_data, _ = cubic_spline(tmp_data,new_wave,tmp_data.shape[-1])
        tmp_data = new_data
    if (limits[0] < min_val) or limits[1] > max_vals[0]:
        new_limits = limits.astype(float)
        new_limits[1] =  new_limits[1] + sep
        clip_range_data = np.arange(*new_limits,sep)[...,np.newaxis]
        
        
        clip_range_data = np.concatenate(
            (clip_range_data, np.zeros((clip_range_data.shape[0],
                                        tmp_data.shape[-1] - 1))),axis = 1)
        begin_idx = np.argwhere(tmp_data[0,0] == clip_range_data)[0,0]
        end_idx = np.argwhere(tmp_data[-1,0] == clip_range_data)[0,0] + 1
        clip_range_data[begin_idx:end_idx,:] = tmp_data
    else:
        clip_range_data = tmp_data
    return clip_range_data




def unit_test():
    relative_paths = [
        'data/OSCONIQ P3030/GT_QSSPA1_13_20190805_spectrum.txt']
    data_list = read_data_from_csv(relative_paths)
    data_list = data_list[0]    
    np.savetxt(f'data/{data_list[1]}',data_list[0],fmt='%.5f',delimiter=',')
    
if __name__ == '__main__':
    unit_test()