"""Functions to add a color bar in geographical figures/maps."""
from typing import Any
import matplotlib.pyplot as plt


def addcbar(
    ax,
    contourf_data,
    ticks_levels,
    position_cbar,
    font_size = 14,
    color_label="#171616",
    orientation = "vertical",
    label_cbar = "none",
    shrink = 1.0,
    pad = 0.05,
    aspect = 30,
) -> Any:
        """Add color bar to plot."""
        cax = ax.inset_axes(position_cbar)
        cbar = plt.colorbar(
            contourf_data,
            cax=cax,
            orientation=orientation,
            pad=pad,
            ax=ax,
            shrink=shrink,
            aspect=aspect,
            ticks=ticks_levels,
        )
        cbar.set_label(label_cbar, fontsize=font_size, color=color_label)
        cbar.ax.set_yticklabels(
            [
                "{:.1f}".format(i) if type(i) == float else "{:.0f}".format(i)
                for i in ticks_levels
            ]
        )
        cbar.ax.tick_params(labelsize=11)

        return cbar

def addcbar_from_arrow_plot(
    ax,
    contourf_data,
    ticks_levels,
    position_cbar,
    font_size = 14,
    color_label="#171616",
    orientation = "vertical",
    label_cbar = "none",
    shrink = 1.0,
    pad = 0.05,
    aspect = 30,
    ) -> Any:
        """Add color bar to arrow plots."""
        cax = ax.inset_axes(position_cbar)
        cbar = plt.colorbar(
            contourf_data,
            cax=cax,
            orientation=orientation,
            pad=pad,
            ax=ax,
            shrink=shrink,
            aspect=aspect,
            ticks=ticks_levels,
        )
        cbar.set_label(label_cbar, fontsize=font_size, color=color_label)
        cbar.ax.set_yticklabels(
            [
                "{:.1f}".format(i) if type(i) == float else "{:.0f}".format(i)
                for i in ticks_levels
            ]
        )
        cbar.ax.tick_params(labelsize=11)

        return cbar