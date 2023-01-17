from scipy.interpolate import CubicSpline
import numpy as np

def cubic_spline(data,
                 new_wave_length,
                 max_idx: int = 4):
    data = data[:, :max_idx]
    new_data = np.zeros((new_wave_length.shape[0],max_idx))
    f_list = []
    new_data[:, 0] = new_wave_length
    for idx in range(1,max_idx,1):
        f = CubicSpline(
            x = data[:, 0].ravel(), y = data[:,idx].ravel()
        )
        new_data[:,idx] = f(new_wave_length)
        f_list.append(f)
    return new_data, f_list


def unittest():
    import matplotlib.pyplot as plt
    x = np.arange(0,1,0.1)
    y = np.sin(x) * x
    z = np.vstack((x,y)).T
    new_x = np.arange(0,1,0.05)
    new_data, _ = cubic_spline(z,new_x,2)
    plt.plot(x,y,'--')
    plt.plot(new_data[:,0],new_data[:,1])
    plt.show()


if __name__ == '__main__':
    unittest()