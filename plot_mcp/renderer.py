import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import numpy as np
from .models import *

# Make output deterministic
matplotlib.rcParams['svg.hashsalt'] = 'plot-mcp'

def _setup_figure(width: float, height: float, title: str = None, x_label: str = None, y_label: str = None, is_polar=False):
    """Setup figure with simplified parameters"""
    # dpi=72 is standard for screen
    dpi = 72
    fig = plt.figure(figsize=(width / dpi, height / dpi), dpi=dpi)
    
    # Transparent background
    fig.patch.set_alpha(0.0)

    # Default margins
    margin_left = 50 / width
    margin_right = 1.0 - (20 / width)
    margin_bottom = 40 / height
    margin_top = 1.0 - (40 / height)
    
    fig.subplots_adjust(left=margin_left, bottom=margin_bottom, right=margin_right, top=margin_top)
    
    if is_polar:
        ax = fig.add_subplot(111, projection='polar')
    else:
        ax = fig.add_subplot(111)

    if title:
        ax.set_title(title)

    # Axis labels
    if not is_polar:
        if x_label:
            ax.set_xlabel(x_label)
        if y_label:
            ax.set_ylabel(y_label)

    return fig, ax

def _finalize(fig, width: float, height: float) -> PlotOutput:
    """Finalize and return plot output"""
    f = io.StringIO()
    fig.savefig(f, format='svg', transparent=True)
    plt.close(fig)
    
    full_svg = f.getvalue()
    
    # Extract <svg ... > ... </svg>
    start_idx = full_svg.find("<svg")
    if start_idx == -1:
        svg_content = full_svg
    else:
        svg_content = full_svg[start_idx:]
    
    return PlotOutput(
        svg=svg_content,
        width=width,
        height=height,
        viewBox=f"0 0 {width} {height}"
    )

def render_line(params: LineParams) -> PlotOutput:
    """Render line plot with flat parameters"""
    fig, ax = _setup_figure(params.width, params.height, params.title, params.x_label, params.y_label)
    
    for series in params.series:
        # Map style names to matplotlib
        mpl_ls = "-"
        if params.line_style == "dashed": 
            mpl_ls = "--"
        elif params.line_style == "dotted": 
            mpl_ls = ":"
            
        ax.plot(
            series.x, 
            series.y, 
            label=series.name, 
            linestyle=mpl_ls, 
            linewidth=params.stroke_width,
            marker='o' if params.show_markers else None
        )
    
    if len(params.series) > 1:
        ax.legend()
        
    return _finalize(fig, params.width, params.height)

def render_scatter(params: ScatterParams) -> PlotOutput:
    """Render scatter plot with flat parameters"""
    fig, ax = _setup_figure(params.width, params.height, params.title, params.x_label, params.y_label)
    
    ax.scatter(
        params.x, params.y,
        s=params.point_radius ** 2,  # s is area
        c=params.color,
        alpha=params.opacity
    )
    
    return _finalize(fig, params.width, params.height)

def render_bar(params: BarParams) -> PlotOutput:
    """Render bar chart with flat parameters"""
    fig, ax = _setup_figure(params.width, params.height, params.title, params.x_label, params.y_label)
    
    if params.orientation == "vertical":
        ax.bar(params.categories, params.values, width=params.bar_width, color=params.color)
    else:
        ax.barh(params.categories, params.values, height=params.bar_width, color=params.color)
        
    return _finalize(fig, params.width, params.height)

def render_area(params: AreaParams) -> PlotOutput:
    """Render area plot with flat parameters"""
    fig, ax = _setup_figure(params.width, params.height, params.title, params.x_label, params.y_label)
    
    ax.fill_between(params.x, params.y, color=params.fill_color, alpha=params.opacity)
    
    return _finalize(fig, params.width, params.height)

def render_histogram(params: HistogramParams) -> PlotOutput:
    """Render histogram with flat parameters"""
    fig, ax = _setup_figure(params.width, params.height, params.title, params.x_label, params.y_label)
    
    ax.hist(
        params.values, 
        bins=params.bins, 
        density=params.density, 
        color=params.color,
        edgecolor='black'
    )
    
    return _finalize(fig, params.width, params.height)

def render_box(params: BoxParams) -> PlotOutput:
    """Render box plot with flat parameters"""
    fig, ax = _setup_figure(params.width, params.height, params.title, params.x_label, params.y_label)
    
    # Prepare data for boxplot
    values = [g.values for g in params.groups]
    labels = [g.name for g in params.groups]
    
    bp = ax.boxplot(
        values, 
        labels=labels, 
        widths=params.box_width, 
        patch_artist=True
    )
    
    for patch in bp['boxes']:
        patch.set_facecolor(params.color)
        
    return _finalize(fig, params.width, params.height)

def render_heatmap(params: HeatmapParams) -> PlotOutput:
    """Render heatmap with flat parameters"""
    fig, ax = _setup_figure(params.width, params.height, params.title)
    
    matrix = np.array(params.matrix)
    
    im = ax.imshow(
        matrix, 
        cmap=params.color_scale,
        aspect='auto'
    )
    
    # Tick labels
    ax.set_xticks(np.arange(len(params.x_labels)), labels=params.x_labels)
    ax.set_yticks(np.arange(len(params.y_labels)), labels=params.y_labels)
    
    # Rotate the tick labels
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    if params.show_values:
        for i in range(len(params.y_labels)):
            for j in range(len(params.x_labels)):
                ax.text(j, i, f"{matrix[i, j]:.2f}",
                       ha="center", va="center", color="w")

    return _finalize(fig, params.width, params.height)

def render_contour(params: ContourParams) -> PlotOutput:
    """Render contour plot with flat parameters"""
    fig, ax = _setup_figure(params.width, params.height, params.title, params.x_label, params.y_label)
    
    X, Y = np.meshgrid(params.x, params.y)
    Z = np.array(params.z)
    
    cs = ax.contour(
        X, Y, Z, 
        levels=params.levels, 
        linewidths=params.stroke_width
    )
    ax.clabel(cs, inline=True, fontsize=10)
    
    return _finalize(fig, params.width, params.height)

def render_pie(params: PieParams) -> PlotOutput:
    """Render pie chart with flat parameters"""
    fig, ax = _setup_figure(params.width, params.height, params.title, is_polar=False)
    
    wedgeprops = {}
    if params.inner_radius_ratio > 0:
        wedgeprops['width'] = 1.0 - params.inner_radius_ratio
        
    ax.pie(
        params.values, 
        labels=params.labels, 
        startangle=params.start_angle,
        wedgeprops=wedgeprops
    )
    
    return _finalize(fig, params.width, params.height)
