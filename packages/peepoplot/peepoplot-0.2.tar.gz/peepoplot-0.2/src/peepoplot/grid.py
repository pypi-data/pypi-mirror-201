import numpy as np
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature


def geoaxes_format(ax, longitude_interval=2.5):
    """
    Format axes with geographic references for cartopy maps.

    Parâmetros
    ----------
    ax: matplotlib.axes._subplots.AxesSubplot
        matplotlib axes to be formatted as geographic axis.

    Retorna
    -------
    gl: cartopy.mpl.geoaxes.GeoAxesSubplot
        geographic axis formatted.
    """
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=1, color='black', alpha=0.3, linestyle='--')
    gl.top_labels = False
    gl.left_labels = True
    gl.right_labels = False
    gl.ylines = True
    gl.xlines = True
    gl.xlocator = mticker.FixedLocator(np.arange(-90,50,10))
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'size': 11}
    gl.ylabel_style = {'size': 11}
    
    estados_br = cfeature.NaturalEarthFeature(category='cultural', scale='50m', facecolor='none', name='admin_1_states_provinces_shp', alpha=.7)
    ax.add_feature(estados_br, edgecolor='gray', linewidth=1)
    ax.add_feature(cartopy.feature.BORDERS, linestyle='-', alpha=.35, edgecolor='gray')

    return gl