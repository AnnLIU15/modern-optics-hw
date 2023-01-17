import matplotlib.pyplot as plt
import colour
from utils import read_data_from_csv
plt.rcParams['figure.figsize'] = (8,8)

xyz_data = read_data_from_csv(csv_path, if_set_limits = False)


data = read_data_from_csv('data\CIE\CIE_illum_D50.csv')[0][0]
plt.plot(data[:,0],data[:,1])
plt.show()
# colour.plotting.diagrams.plot_chromaticity_diagram_colours(samples=4096,diagram_colours="xyz")