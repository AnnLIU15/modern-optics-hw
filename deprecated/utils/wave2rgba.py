
import numpy as np
from typing import Union, List

def wavelength_to_rgba(wave_length: Union[List,float,int,np.ndarray],
                      gamma: float = 0.8) -> np.ndarray:
    r'''rewrite the FORTRAN code to python (380nm~780nm)
    http://www.physics.sfasu.edu/astro/color/spectra.html
    del ~~(Additionally alpha value set to 0.5 outside range)~~
    
    Args:
        wave_length (Union[List,float,int,np.ndarray]): _description_
        gamma (float, optional): _description_. Defaults to 0.8.

    Raises:
        TypeError: _description_
        ValueError: _description_

    Returns:
        np.ndarray: _description_
    '''
    if isinstance(wave_length, float) or \
        isinstance(wave_length, int):
        wave_length = np.array([wave_length])
    elif isinstance(wave_length, list) :
        wave_length = np.array(wave_length)
    elif isinstance(wave_length, np.ndarray):
        pass
    else:
        raise TypeError(f'Undefine wave_length input type: {type(wave_length)}')
    
    data_len =  len(wave_length)
    RGBA_array = np.zeros((data_len,4),dtype=float)
    RGBA_array[:,3] = np.where(
        np.logical_and(wave_length > 780,wave_length < 380),0.5,1)
    wave_length = np.clip(wave_length, 380, 780)
    for cur_idx, cur_wave in enumerate(wave_length):
        if cur_wave <= 440:
            # RGB
            RGBA_array[cur_idx,:3] = [-1.*(cur_wave-440.)/(440.-380.), 0.0, 1.0]
        elif cur_wave <= 490:
            RGBA_array[cur_idx,:3] = [0.0, (cur_wave-440.)/(490.-440.), 1.0]
        elif cur_wave <= 510:
            RGBA_array[cur_idx,:3] = [0.0, 1, -1.*(cur_wave-510.)/(510.-490.)]
        elif cur_wave <= 580:
            RGBA_array[cur_idx,:3] = [(cur_wave-510.)/(580.-510.), 1.0, 0.0]
           
        elif cur_wave <= 645:
            RGBA_array[cur_idx,:3] = [1, -1.*(cur_wave-645.)/(645.-580.), 0.0]
        elif cur_wave <= 780:
            RGBA_array[cur_idx,:3] = [1, 0.0, 0.0]
        else:
            raise ValueError(f'Something Wrong value: {cur_wave}')
        # LET THE INTENSITY SSS FALL OFF NEAR THE VISION LIMITS
        if cur_wave > 700:
            scale = 0.3 + 0.7 * (780 - cur_wave)/(780 - 700)
        elif cur_wave < 420:
            scale = 0.3 + 0.7*(cur_wave-380.)/(420.-380.)
        else:
            scale = 1
        # GAMMA ADJUST AND WRITE IMAGE TO AN ARRAY
        RGBA_array[cur_idx,:3] = (scale * RGBA_array[cur_idx,:3])**gamma
    return RGBA_array
