import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import numpy as np
from .models import *

# Make output deterministic
matplotlib.rcParams['svg.hashsalt'] = 'plot-mcp'

def _setup_figure(config: BaseConfig, is_polar=False):
    # dpi=72 is standard for screen
    dpi = 72
    fig = plt.figure(figsize=(config.width / dpi, config.height / dpi), dpi=dpi)
    
    if config.background and config.background != "transparent":
        fig.patch.set_facecolor(config.background)
    else:
        fig.patch.set_alpha(0.0)

    # Compute margins in fractions
    left = config.margin.left / config.width
    right = 1.0 - (config.margin.right / config.width)
    bottom = config.margin.bottom / config.height
    top = 1.0 - (config.margin.top / config.height)

    # Avoid invalid margins
    if left >= right or bottom >= top:
        # Fallback to defaults or error?
        # Let's clamp to safe values
        left = min(left, 0.45)
        right = max(right, 0.55)
        bottom = min(bottom, 0.45)
        top = max(top, 0.55)
    
    fig.subplots_adjust(left=left, bottom=bottom, right=right, top=top)
    
    if is_polar:
        ax = fig.add_subplot(111, projection='polar')
    else:
        ax = fig.add_subplot(111)

    if config.title:
        ax.set_title(config.title)

    # Axis setup (skip for pie/polar mostly, but common logic here)
    if not is_polar:
        if config.x_axis:
            if config.x_axis.label:
                ax.set_xlabel(config.x_axis.label)
            ax.set_xscale(config.x_axis.scale)
            if config.x_axis.min is not None:
                ax.set_xlim(left=config.x_axis.min)
            if config.x_axis.max is not None:
                ax.set_xlim(right=config.x_axis.max)
        
        if config.y_axis:
            if config.y_axis.label:
                ax.set_ylabel(config.y_axis.label)
            ax.set_yscale(config.y_axis.scale)
            if config.y_axis.min is not None:
                ax.set_ylim(bottom=config.y_axis.min)
            if config.y_axis.max is not None:
                ax.set_ylim(top=config.y_axis.max)

    return fig, ax

def _finalize(fig, config: BaseConfig) -> PlotOutput:
    f = io.StringIO()
    fig.savefig(f, format='svg', transparent=(config.background == "transparent"))
    plt.close(fig)
    
    full_svg = f.getvalue()
    
    # Extract <svg ... > ... </svg>
    # Also strip default explicit width/height in pt/px if we want to be clean, 
    # but the prompt just says "svg rules: valid standalone svg".
    # Matplotlib's output is valid standalone.
    
    start_idx = full_svg.find("<svg")
    if start_idx == -1:
        # Fallback, should not happen
        svg_content = full_svg
    else:
        svg_content = full_svg[start_idx:]
    
    return PlotOutput(
        svg=svg_content,
        width=config.width,
        height=config.height,
        viewBox=f"0 0 {config.width} {config.height}"
    )

def render_line(data: LineData, config: LineConfig) -> PlotOutput:
    fig, ax = _setup_figure(config)
    
    for series in data.series:
        ls = config.line_style
        # Map style names to matplotlib
        mpl_ls = "-"
        if ls == "dashed": mpl_ls = "--"
        elif ls == "dotted": mpl_ls = ":"
            
        ax.plot(
            series.x, 
            series.y, 
            label=series.name, 
            linestyle=mpl_ls, 
            linewidth=config.stroke_width,
            marker='o' if config.show_markers else None
        )
    
    if len(data.series) > 1:
        ax.legend()
        
    return _finalize(fig, config)

def render_scatter(data: ScatterData, config: ScatterConfig) -> PlotOutput:
    fig, ax = _setup_figure(config)
    
    xs = [p.x for p in data.points]
    ys = [p.y for p in data.points]
    
    ax.scatter(
        xs, ys,
        s=config.point_radius ** 2, # s is area
        c=config.color,
        alpha=config.opacity
    )
    
    return _finalize(fig, config)

def render_bar(data: BarData, config: BarConfig) -> PlotOutput:
    fig, ax = _setup_figure(config)
    
    # Matplotlib bars are centered by default.
    # config.bar_width defaults to 0.8
    
    if config.orientation == "vertical":
        ax.bar(data.categories, data.values, width=config.bar_width, color=config.color)
    else:
        ax.barh(data.categories, data.values, height=config.bar_width, color=config.color)
        
    return _finalize(fig, config)

def render_area(data: AreaData, config: AreaConfig) -> PlotOutput:
    fig, ax = _setup_figure(config)
    
    ax.fill_between(data.x, data.y, color=config.fill_color, alpha=config.opacity)
    # Usually also plot the line on top? Spec doesn't say. 
    # "Render filled area under a curve".
    # Usually implies starting from 0 (or bottom).
    
    return _finalize(fig, config)

def render_histogram(data: HistogramData, config: HistogramConfig) -> PlotOutput:
    fig, ax = _setup_figure(config)
    
    ax.hist(
        data.values, 
        bins=config.bins, 
        density=config.density, 
        color=config.color,
        edgecolor='black' # Usually looks better
    )
    
    return _finalize(fig, config)

def render_box(data: BoxData, config: BoxConfig) -> PlotOutput:
    fig, ax = _setup_figure(config)
    
    # Prepare data for boxplot
    # boxplot expects a list of arrays
    values = [g.values for g in data.groups]
    labels = [g.name for g in data.groups]
    
    # Customizing boxplot colors is a bit verbose in mpl
    bp = ax.boxplot(
        values, 
        labels=labels, 
        widths=config.box_width, 
        patch_artist=True
    )
    
    for patch in bp['boxes']:
        patch.set_facecolor(config.color)
        
    return _finalize(fig, config)

def render_heatmap(data: HeatmapData, config: HeatmapConfig) -> PlotOutput:
    fig, ax = _setup_figure(config)
    
    matrix = np.array(data.matrix)
    
    im = ax.imshow(
        matrix, 
        cmap=config.color_scale, # viridis, plasma, gray are valid mpl cmaps
        aspect='auto' # or 'equal'? 'auto' fits the axes box
    )
    
    # Tic labels
    ax.set_xticks(np.arange(len(data.x_labels)), labels=data.x_labels)
    ax.set_yticks(np.arange(len(data.y_labels)), labels=data.y_labels)
    
    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    if config.show_values:
        for i in range(len(data.y_labels)):
            for j in range(len(data.x_labels)):
                ax.text(j, i, f"{matrix[i, j]:.2f}",
                       ha="center", va="center", color="w") # color might need contrast check...

    return _finalize(fig, config)

def render_contour(data: ContourData, config: ContourConfig) -> PlotOutput:
    fig, ax = _setup_figure(config)
    
    X, Y = np.meshgrid(data.x, data.y)
    Z = np.array(data.z)
    
    cs = ax.contour(
        X, Y, Z, 
        levels=config.levels, 
        linewidths=config.stroke_width
    )
    ax.clabel(cs, inline=True, fontsize=10)
    
    return _finalize(fig, config)

def render_pie(data: PieData, config: PieConfig) -> PlotOutput:
    # use polar? or just ax.pie
    fig, ax = _setup_figure(config, is_polar=False)
    # pie creates its own aspect ratio
    
    # "inner_radius_ratio": 0.0 = full pie, >0 = donut
    # mpl pie takes 'wedgeprops=dict(width=...)'? NO.
    # pie(x, explode=None, labels=None, autopct=None, pctdistance=0.6, shadow=False, labeldistance=1.1, startangle=0, radius=1, counterclock=True, wedgeprops=None, textprops=None, center=(0, 0), frame=False, rotatelabels=False, *, normalize=True, data=None)
    
    # If inner_radius_ratio > 0, we can use wedgeprops={'width': ...}
    # radius=1. width = radius - inner_radius. 
    # If inner_ratio is 0.4, inner radius is 0.4. Outer is 1. Width is 0.6.
    
    wedgeprops = {}
    if config.inner_radius_ratio > 0:
        wedgeprops['width'] = 1.0 - config.inner_radius_ratio
        
    ax.pie(
        data.values, 
        labels=data.labels, 
        startangle=config.start_angle,
        wedgeprops=wedgeprops
    )
    
    return _finalize(fig, config)
