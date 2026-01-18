import os
import click
import datetime
import uuid
from typing import Optional
from fastmcp import FastMCP
from .models import (
    LineData, LineConfig, ScatterData, ScatterConfig,
    BarData, BarConfig, AreaData, AreaConfig,
    HistogramData, HistogramConfig, BoxData, BoxConfig,
    HeatmapData, HeatmapConfig, ContourData, ContourConfig,
    PieData, PieConfig, PlotOutput
)
from .renderer import (
    render_line, render_scatter, render_bar, render_area,
    render_histogram, render_box, render_heatmap,
    render_contour, render_pie
)

mcp = FastMCP("PlotMCP")

# Global configuration for output directory
OUTPUT_DIR: Optional[str] = None

def save_svg_and_update_output(output: PlotOutput, tool_name: str, config) -> PlotOutput:
    """Save SVG to file and return path if OUTPUT_DIR is configured, otherwise keep SVG content."""
    if not OUTPUT_DIR:
        return output
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Generate a filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    title_slug = "".join(c if c.isalnum() else "_" for c in (config.title or ""))[:30]
    filename = f"{tool_name}_{timestamp}_{title_slug or uuid.uuid4().hex[:8]}.svg"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(output.svg or "")
    
    output.svg_path = filepath
    output.svg = None  # Remove SVG content from response to LLM
    return output

@mcp.tool()
def plot_line(data: LineData, config: LineConfig = LineConfig()) -> PlotOutput:
    """Render one or more continuous 2D lines. Returns file path if output-dir is configured."""
    res = render_line(data, config)
    return save_svg_and_update_output(res, "line", config)

@mcp.tool()
def plot_scatter(data: ScatterData, config: ScatterConfig = ScatterConfig()) -> PlotOutput:
    """Render discrete 2D points. Returns file path if output-dir is configured."""
    res = render_scatter(data, config)
    return save_svg_and_update_output(res, "scatter", config)

@mcp.tool()
def plot_bar(data: BarData, config: BarConfig = BarConfig()) -> PlotOutput:
    """Render categorical bar chart. Returns file path if output-dir is configured."""
    res = render_bar(data, config)
    return save_svg_and_update_output(res, "bar", config)

@mcp.tool()
def plot_area(data: AreaData, config: AreaConfig = AreaConfig()) -> PlotOutput:
    """Render filled area under a curve. Returns file path if output-dir is configured."""
    res = render_area(data, config)
    return save_svg_and_update_output(res, "area", config)

@mcp.tool()
def plot_histogram(data: HistogramData, config: HistogramConfig = HistogramConfig()) -> PlotOutput:
    """Render 1D histogram. Returns file path if output-dir is configured."""
    res = render_histogram(data, config)
    return save_svg_and_update_output(res, "histogram", config)

@mcp.tool()
def plot_box(data: BoxData, config: BoxConfig = BoxConfig()) -> PlotOutput:
    """Render box plot from raw values. Returns file path if output-dir is configured."""
    res = render_box(data, config)
    return save_svg_and_update_output(res, "box", config)

@mcp.tool()
def plot_heatmap(data: HeatmapData, config: HeatmapConfig = HeatmapConfig()) -> PlotOutput:
    """Render 2D matrix as color grid. Returns file path if output-dir is configured."""
    res = render_heatmap(data, config)
    return save_svg_and_update_output(res, "heatmap", config)

@mcp.tool()
def plot_contour(data: ContourData, config: ContourConfig = ContourConfig()) -> PlotOutput:
    """Render 2D contour lines from grid data. Returns file path if output-dir is configured."""
    res = render_contour(data, config)
    return save_svg_and_update_output(res, "contour", config)

@mcp.tool()
def plot_pie(data: PieData, config: PieConfig = PieConfig()) -> PlotOutput:
    """Render circular pie chart. Returns file path if output-dir is configured."""
    res = render_pie(data, config)
    return save_svg_and_update_output(res, "pie", config)

@click.command()
@click.option("--output-dir", type=click.Path(), help="Directory to save generated SVG files.")
@click.option("--transport", type=click.Choice(["stdio", "sse", "streamable-http"]), default="stdio", help="Transport type.")
@click.option("--port", type=int, default=8000, help="Port for SSE/HTTP transport.")
def main(output_dir: Optional[str], transport: str, port: int):
    global OUTPUT_DIR
    if output_dir:
        OUTPUT_DIR = os.path.abspath(output_dir)
        os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    if transport == "stdio":
        mcp.run(transport="stdio")
    elif transport == "sse":
        mcp.run(transport="sse", port=port)
    elif transport == "streamable-http":
        mcp.run(transport="streamable-http", port=port)

if __name__ == "__main__":
    main()
