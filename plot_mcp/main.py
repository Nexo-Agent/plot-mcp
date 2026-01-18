import os
import click
import datetime
import uuid
from typing import Optional, Union
from fastmcp import FastMCP
from .models import (
    LineParams, ScatterParams, BarParams, AreaParams,
    HistogramParams, BoxParams, HeatmapParams, ContourParams,
    PieParams, PlotOutput
)
from .renderer import (
    render_line, render_scatter, render_bar, render_area,
    render_histogram, render_box, render_heatmap,
    render_contour, render_pie
)

mcp = FastMCP("PlotMCP")

# Global configuration for output directory
OUTPUT_DIR: Optional[str] = None

def save_svg_and_update_output(output: PlotOutput, tool_name: str, title: str = None):
    """Save SVG to file and return formatted path if OUTPUT_DIR is configured, otherwise keep SVG content."""
    if not OUTPUT_DIR:
        return output
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Generate a filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    title_slug = "".join(c if c.isalnum() else "_" for c in (title or ""))[:30]
    filename = f"{tool_name}_{timestamp}_{title_slug or uuid.uuid4().hex[:8]}.svg"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(output.svg or "")
    
    # Return formatted string for client to parse and display
    return f"```local_image\n{filepath}\n```"

@mcp.tool()
def plot_line(params: LineParams) -> Union[PlotOutput, str]:
    """Render one or more continuous 2D lines. Simple flat parameters - no nested objects!
    
    Example:
    {
        "series": [{"name": "Line 1", "x": [1, 2, 3], "y": [1, 4, 9]}],
        "title": "My Plot",
        "width": 800,
        "height": 400
    }
    """
    res = render_line(params)
    return save_svg_and_update_output(res, "line", params.title)

@mcp.tool()
def plot_scatter(params: ScatterParams) -> Union[PlotOutput, str]:
    """Render discrete 2D points. Simple flat parameters - no nested objects!
    
    Example:
    {
        "x": [1, 2, 3, 4],
        "y": [1, 4, 9, 16],
        "title": "Scatter Plot",
        "color": "steelblue"
    }
    """
    res = render_scatter(params)
    return save_svg_and_update_output(res, "scatter", params.title)

@mcp.tool()
def plot_bar(params: BarParams) -> Union[PlotOutput, str]:
    """Render categorical bar chart. Simple flat parameters - no nested objects!
    
    Example:
    {
        "categories": ["A", "B", "C"],
        "values": [10, 20, 15],
        "title": "Bar Chart",
        "orientation": "vertical"
    }
    """
    res = render_bar(params)
    return save_svg_and_update_output(res, "bar", params.title)

@mcp.tool()
def plot_area(params: AreaParams) -> Union[PlotOutput, str]:
    """Render filled area under a curve. Simple flat parameters - no nested objects!
    
    Example:
    {
        "x": [1, 2, 3, 4],
        "y": [1, 4, 9, 16],
        "title": "Area Plot",
        "fill_color": "steelblue"
    }
    """
    res = render_area(params)
    return save_svg_and_update_output(res, "area", params.title)

@mcp.tool()
def plot_histogram(params: HistogramParams) -> Union[PlotOutput, str]:
    """Render 1D histogram. Simple flat parameters - no nested objects!
    
    Example:
    {
        "values": [1, 2, 2, 3, 3, 3, 4, 4, 5],
        "bins": 5,
        "title": "Histogram"
    }
    """
    res = render_histogram(params)
    return save_svg_and_update_output(res, "histogram", params.title)

@mcp.tool()
def plot_box(params: BoxParams) -> Union[PlotOutput, str]:
    """Render box plot from raw values. Simple flat parameters - no nested objects!
    
    Example:
    {
        "groups": [
            {"name": "Group A", "values": [1, 2, 3, 4, 5]},
            {"name": "Group B", "values": [2, 3, 4, 5, 6]}
        ],
        "title": "Box Plot"
    }
    """
    res = render_box(params)
    return save_svg_and_update_output(res, "box", params.title)

@mcp.tool()
def plot_heatmap(params: HeatmapParams) -> Union[PlotOutput, str]:
    """Render 2D matrix as color grid. Simple flat parameters - no nested objects!
    
    Example:
    {
        "matrix": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        "x_labels": ["X1", "X2", "X3"],
        "y_labels": ["Y1", "Y2", "Y3"],
        "title": "Heatmap"
    }
    """
    res = render_heatmap(params)
    return save_svg_and_update_output(res, "heatmap", params.title)

@mcp.tool()
def plot_contour(params: ContourParams) -> Union[PlotOutput, str]:
    """Render 2D contour lines from grid data. Simple flat parameters - no nested objects!
    
    Example:
    {
        "x": [1, 2, 3],
        "y": [1, 2, 3],
        "z": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        "title": "Contour Plot"
    }
    """
    res = render_contour(params)
    return save_svg_and_update_output(res, "contour", params.title)

@mcp.tool()
def plot_pie(params: PieParams) -> Union[PlotOutput, str]:
    """Render circular pie chart. Simple flat parameters - no nested objects!
    
    Example:
    {
        "labels": ["A", "B", "C"],
        "values": [30, 50, 20],
        "title": "Pie Chart"
    }
    """
    res = render_pie(params)
    return save_svg_and_update_output(res, "pie", params.title)

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
