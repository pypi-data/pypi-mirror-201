"""Functions to plot some types of geographical figures/maps."""
from typing import Union
from typing import List
from typing import Any
import matplotlib
import matplotlib.pyplot as plt
from cartopy import crs as ccrs
from cartopy.feature import BORDERS


def generate_figure(
    figsize,
    title_left_text: str = "",
    title_right_text: str = "",
    title_font : Any = "",
    title_fontsize : int = "",
    title_color : str = "#171616",
    coordinates_to_clipe: Union[ List[float], None] = None,
    ):
    fig, ax = plt.subplots(
        subplot_kw=dict(projection=ccrs.PlateCarree()), figsize=figsize
    )

    ax.coastlines(zorder=10)
    ax.add_feature(BORDERS, linestyle="-", alpha=0.5, zorder=10)
    ax.set_facecolor("white")

    ax.set_extent(coordinates_to_clipe) if not coordinates_to_clipe is None else None

    ax.set_title(
        title_left_text,
        font=title_font,
        fontsize=title_fontsize,
        loc="left",
        color=title_color,
    )
    ax.set_title(
        title_right_text,
        font=title_font,
        fontsize=title_fontsize,
        loc="right",
        color=title_color,
    )
    fig.patch.set_facecolor("white")
    return (fig,ax)


def plot_contourf(
        ax,
        lon,
        lat,
        dataset,
        norm,
        levels,
        cmap,
        extend = "both",
        transform=ccrs.PlateCarree()) -> matplotlib.axes:
    """
    Generate a geographic map with filled outline.

    Parameters
    ----------
    ax : Matplotli.axes
        Subplots axes object from matplolib.
    lon : _type_
        Selected longitudes from dataset file.
    lat : _type_
        Selected latitudes from dataset file.
    dataset : _type_
        Dataset with data to plot.
    norm : _type_
        Normalization of color scale.
    levels : _type_
        Levels to plot variable in crescent order.
    cmap : _type_
        color map from matplotlib.
    extend : str, optional
        _description_, by default "both"
    transform : _type_, optional
        Geographic transformation, by default ccrs.PlateCarree()

    Returns
    -------
    matplotlib.axes
        _description_
    """
    cont = ax.contourf(
        lon,
        lat,
        dataset,
        norm = norm,
        levels = levels,
        cmap = cmap,
        extend = extend,
        transform = transform,
    )
    return cont

def plot_pcolormesh(
        ax,
        lon,
        lat,
        dataset,
        levels,
        cmap,
        transform=ccrs.PlateCarree()) -> matplotlib.axes:
    """
    Generate a geographic map with squares centered on grid points.

    Parameters
    ----------
    ax : _type_
        _description_
    lon : _type_
        _description_
    lat : _type_
        _description_
    dataset : _type_
        _description_
    levels : _type_
        _description_
    cmap : _type_
        _description_
    transform : _type_, optional
        _description_, by default ccrs.PlateCarree()

    Returns
    -------
    matplotlib.axes
        _description_
    """
    cont = ax.pcolormesh(
            lon, 
            lat,
            dataset,
            shading="nearest",
            vmin=levels[0],
            vmax=levels[-1],
            cmap=cmap,
            #transform=ccrs.PlateCarree(),
        )


def plot_contourlines_numberlines(
        ax,
        lon,
        lat,
        dataset,
        norm,
        levels,
        contour_line_color,
        linewidths,
        fontzise_number_contourline,
        inline = True,
        transform=ccrs.PlateCarree()) -> matplotlib.axes:
    """
    Plot isohyet lines (contourlines) with a number on lines. 

    Parameters
    ----------
    ax : _type_
        _description_
    lon : _type_
        _description_
    lat : _type_
        _description_
    dataset : _type_
        _description_
    norm : _type_
        _description_
    levels : _type_
        _description_
    contour_line_color : _type_
        _description_
    linewidths : _type_
        _description_
    fontzise_number_contourline : _type_
        _description_
    inline : bool, optional
        _description_, by default True
    transform : _type_, optional
        _description_, by default ccrs.PlateCarree()

    Returns
    -------
    matplotlib.axes
        _description_
    """
    contour_line = ax.contour(
            lon,
            lat,
            dataset,
            norm=norm,
            levels=levels,
            colors=contour_line_color,
            linewidths=linewidths,
            transform=transform,
        )
    
    numbers_on_lines = ax.clabel(
            contour_line,
            levels,
            inline=inline,
            fontsize=fontzise_number_contourline,
        )
    
    return contour_line, numbers_on_lines

    
def plot_vectors(
        ax,
        lonx,
        laty,
        datasetx,
        datasety,
        linewidth_arrows,
        arrowsize,
        density_arrows,
        color_arrows,
        transform=ccrs.PlateCarree(),
        ) -> matplotlib.axes:
    """
    Plot a map of arrow-lines.

    Parameters
    ----------
    ax : _type_
        _description_
    lonx : _type_
        _description_
    laty : _type_
        _description_
    datasetx : _type_
        _description_
    datasety : _type_
        _description_
    linewidth_arrows : _type_
        _description_
    arrowsize : _type_
        _description_
    density_arrows : _type_
        _description_
    color_arrows : _type_
        _description_
    transform : _type_, optional
        _description_, by default ccrs.PlateCarree()

    Returns
    -------
    matplotlib.axes
        _description_
    """
    sp = ax.streamplot(
            lonx,
            laty,
            datasetx,
            datasety,
            linewidth=linewidth_arrows,
            arrowsize=arrowsize,
            density=density_arrows,
            color=color_arrows,
            transform=ccrs.PlateCarree(),
        )
    
    return sp

