from typing import List, Literal, Optional, Any
from pydantic import BaseModel, Field

# --- Shared Config ---

class Margin(BaseModel):
    top: float = 40
    right: float = 20
    bottom: float = 40
    left: float = 50

class AxisConfig(BaseModel):
    label: Optional[str] = None
    scale: Literal["linear", "log", "symlog"] = "linear"
    min: Optional[float] = None
    max: Optional[float] = None

class BaseConfig(BaseModel):
    title: Optional[str] = None
    width: float = 800
    height: float = 400
    background: str = "transparent"
    margin: Margin = Field(default_factory=Margin)
    x_axis: Optional[AxisConfig] = Field(default_factory=AxisConfig)
    y_axis: Optional[AxisConfig] = Field(default_factory=AxisConfig)

# --- Tool Specific Configs & Data ---

# 1. plot_line
class LineSeries(BaseModel):
    name: str
    x: List[float]
    y: List[float]

class LineData(BaseModel):
    series: List[LineSeries]

class LineConfig(BaseConfig):
    line_style: Literal["solid", "dashed", "dotted"] = "solid"
    stroke_width: float = 2
    show_markers: bool = False

# 2. plot_scatter
class Point(BaseModel):
    x: float
    y: float

class ScatterData(BaseModel):
    points: List[Point]

class ScatterConfig(BaseConfig):
    point_radius: float = 4
    color: str = "black"
    opacity: float = 1.0

# 3. plot_bar
class BarData(BaseModel):
    categories: List[str]
    values: List[float]

class BarConfig(BaseConfig):
    orientation: Literal["vertical", "horizontal"] = "vertical"
    bar_width: float = 0.8
    color: str = "steelblue"

# 4. plot_area
class AreaData(BaseModel):
    x: List[float]
    y: List[float]

class AreaConfig(BaseConfig):
    fill_color: str = "steelblue"
    opacity: float = 0.6

# 5. plot_histogram
class HistogramData(BaseModel):
    values: List[float]

class HistogramConfig(BaseConfig):
    bins: int = 10
    density: bool = False
    color: str = "steelblue"

# 6. plot_box
class BoxGroup(BaseModel):
    name: str
    values: List[float]

class BoxData(BaseModel):
    groups: List[BoxGroup]

class BoxConfig(BaseConfig):
    box_width: float = 0.6
    color: str = "black"

# 7. plot_heatmap
class HeatmapData(BaseModel):
    matrix: List[List[float]]
    x_labels: List[str]
    y_labels: List[str]

class HeatmapConfig(BaseConfig):
    color_scale: Literal["viridis", "plasma", "gray"] = "viridis"
    show_values: bool = False

# 8. plot_contour
class ContourData(BaseModel):
    x: List[float]
    y: List[float]
    z: List[List[float]]

class ContourConfig(BaseConfig):
    levels: int = 10
    stroke_width: float = 1

# 9. plot_pie
class PieData(BaseModel):
    labels: List[str]
    values: List[float]

class PieConfig(BaseConfig):
    inner_radius_ratio: float = 0.0
    start_angle: float = 0

# --- Response ---
class PlotOutput(BaseModel):
    svg_path: Optional[str] = None
    svg: Optional[str] = None
    width: float
    height: float
    viewBox: str
