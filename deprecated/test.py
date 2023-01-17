import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
from utils.wave2rgba import wavelength_to_rgba
import matplotlib.patches as patches


clim=(380,780)
norm = plt.Normalize(*clim)
wl = np.arange(clim[0],clim[1]+1,1)
colorlist = wavelength_to_rgba(wl,0.8)

spectralmap = matplotlib.colors.LinearSegmentedColormap.from_list("spectrum", colorlist)

fig, axs = plt.subplots(1, 1, figsize=(8,4), tight_layout=True)

wavelengths = np.linspace(380, 780, 2048)
spectrum = (5 + np.sin(wavelengths*0.1)**2) * np.exp(-0.00002*(wavelengths-600)**2)
plt.plot(wavelengths, spectrum, color='darkred')

y = np.linspace(0, np.max(spectrum), 100)

X,Y = np.meshgrid(wavelengths, y)

extent=(np.min(wavelengths), np.max(wavelengths), np.min(y), np.max(y))

axes = plt.gca()
polygon = patches.Polygon(
        np.vstack(
            [
                (clim[0], 0),
                np.hstack((wavelengths[:,np.newaxis],spectrum[:,np.newaxis])),
                (clim[1], 0),
            ]
        ),
        facecolor="none",
        edgecolor="none",
        zorder=-140
    )
axes.add_patch(polygon)
padding = 0.1
axes.bar(
        x=wl - padding,
        height=max(y),
        width=1 + padding,
        color=colorlist[:,:3],
        align="edge",
        clip_path=polygon,
        zorder=-140
    )
# im = plt.imshow(X, clim=clim,  extent=extent, cmap=spectralmap, aspect='auto')
# im.set_clip_path(polygon)
# plt.fill_between(wavelengths, spectrum, 8, color='w', interpolate=True)
plt.xlabel('Wavelength (nm)')
plt.ylabel('Intensity')
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.get_yaxis().set_visible(False)
ax.legend(frameon = False)

plt.savefig('WavelengthColors.png', format = 'svg', dpi = 300,
                    bbox_inches='tight',pad_inches = 0,transparent = True)

plt.show()