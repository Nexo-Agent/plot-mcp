from typing import List, Literal, Optional
from pydantic import BaseModel, Field

# --- Simple, Flat Models for Each Tool ---

# 1. plot_line - Simple flat structure
class LineSeries(BaseModel):
    """A single line series with name and data points"""
    name: str
    x: List[float]
    y: List[float]

class LineParams(BaseModel):
    """All parameters for line plot in one flat structure"""
    series: List[LineSeries]
    title: Optional[str] = None
    width: float = 800
    height: float = 400
    line_style: Literal["solid", "dashed", "dotted"] = "solid"
    stroke_width: float = 2
    show_markers: bool = False
    x_label: Optional[str] = None
    y_label: Optional[str] = None

# 2. plot_scatter - Simple flat structure
class ScatterParams(BaseModel):
    """All parameters for scatter plot in one flat structure"""
    x: List[float]
    y: List[float]
    title: Optional[str] = None
    width: float = 800
    height: float = 400
    point_radius: float = 4
    color: str = "steelblue"
    opacity: float = 1.0
    x_label: Optional[str] = None
    y_label: Optional[str] = None

# 3. plot_bar - Simple flat structure
class BarParams(BaseModel):
    """All parameters for bar chart in one flat structure"""
    categories: List[str]
    values: List[float]
    title: Optional[str] = None
    width: float = 800
    height: float = 400
    orientation: Literal["vertical", "horizontal"] = "vertical"
    bar_width: float = 0.8
    color: str = "steelblue"
    x_label: Optional[str] = None
    y_label: Optional[str] = None

# 4. plot_area - Simple flat structure
class AreaParams(BaseModel):
    """All parameters for area plot in one flat structure"""
    x: List[float]
    y: List[float]
    title: Optional[str] = None
    width: float = 800
    height: float = 400
    fill_color: str = "steelblue"
    opacity: float = 0.6
    x_label: Optional[str] = None
    y_label: Optional[str] = None

# 5. plot_histogram - Simple flat structure
class HistogramParams(BaseModel):
    """All parameters for histogram in one flat structure"""
    values: List[float]
    title: Optional[str] = None
    width: float = 800
    height: float = 400
    bins: int = 10
    density: bool = False
    color: str = "steelblue"
    x_label: Optional[str] = None
    y_label: Optional[str] = None

# 6. plot_box - Simple flat structure
class BoxGroup(BaseModel):
    """A single box plot group"""
    name: str
    values: List[float]

class BoxParams(BaseModel):
    """All parameters for box plot in one flat structure"""
    groups: List[BoxGroup]
    title: Optional[str] = None
    width: float = 800
    height: float = 400
    box_width: float = 0.6
    color: str = "black"
    x_label: Optional[str] = None
    y_label: Optional[str] = None

# 7. plot_heatmap - Simple flat structure
class HeatmapParams(BaseModel):
    """All parameters for heatmap in one flat structure"""
    matrix: List[List[float]]
    x_labels: List[str]
    y_labels: List[str]
    title: Optional[str] = None
    width: float = 800
    height: float = 400
    color_scale: Literal["viridis", "plasma", "gray"] = "viridis"
    show_values: bool = False

# 8. plot_contour - Simple flat structure
class ContourParams(BaseModel):
    """All parameters for contour plot in one flat structure"""
    x: List[float]
    y: List[float]
    z: List[List[float]]
    title: Optional[str] = None
    width: float = 800
    height: float = 400
    levels: int = 10
    stroke_width: float = 1
    x_label: Optional[str] = None
    y_label: Optional[str] = None

# 9. plot_pie - Simple flat structure
class PieParams(BaseModel):
    """All parameters for pie chart in one flat structure"""
    labels: List[str]
    values: List[float]
    title: Optional[str] = None
    width: float = 800
    height: float = 400
    inner_radius_ratio: float = 0.0
    start_angle: float = 0

# --- Response ---
class PlotOutput(BaseModel):
    svg_path: Optional[str] = None
    svg: Optional[str] = None
    width: float
    height: float
    viewBox: str
