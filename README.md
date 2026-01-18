# PlotMCP Server

PlotMCP is a powerful Model Context Protocol (MCP) server designed to enable LLMs to generate high-quality SVG charts from structured data. It leverages `fastmcp` for the server infrastructure and `matplotlib` for consistent, precise chart rendering.

## Key Features

- **Pure SVG Rendering**: Generates static SVG format with no external JavaScript dependencies. Safe, portable, and easy to embed.
- **Multiple Plot Types**: Supports Line, Scatter, Bar, Area, Histogram, Box, Heatmap, Contour, and Pie charts.
- **Flexible Configuration**: Full control over titles, dimensions, margins, and axis properties (linear, log, and symlog scales).
- **Output Management**: Automatically saves generated charts to a specified directory and returns the file path to the LLM.
- **Deterministic Output**: Ensures identical inputs produce bit-identical SVG outputs.

## Installation

Requires Python >= 3.11 and `uv` installed.

### Local Installation (Development)

```bash
git clone <repository-url>
cd plot-mcp
uv sync
```

### Install as a Global Tool

```bash
uv tool install .
```

## Running the Server

### Running from Source

```bash
uv run plot-mcp --output-dir ./plots
```

### Running Remotely via GitHub (using `uvx`)

You can run the server directly from the GitHub repository without manual cloning:

```bash
uvx --from git+https://github.com/Nexo-Agent/plot-mcp plot-mcp --output-dir ./plots
```

_Note: Replace the URL with the actual repository location._

## CLI Configuration

The server supports the following command-line options:

- `--output-dir PATH`: Directory where generated SVG files will be saved. When set, tools return the file path instead of the raw SVG content.
- `--transport [stdio|sse|streamable-http]`: The communication protocol (default: `stdio`).
- `--port INTEGER`: The port for SSE or HTTP transport (default: 8000).

## Available Tools

The LLM can invoke the following tools:

1. `plot_line`: Render continuous 2D lines.
2. `plot_scatter`: Render discrete 2D points.
3. `plot_bar`: Render categorical bar charts.
4. `plot_area`: Render filled area under a curve.
5. `plot_histogram`: Render 1D histograms.
6. `plot_box`: Render box plots from raw values.
7. `plot_heatmap`: Render 2D matrix as a color grid.
8. `plot_contour`: Render 2D contour lines.
9. `plot_pie`: Render circular pie and donut charts.

## Chart Configuration

All tools accept a shared `config` object to customize the visual output:

```json
{
  "title": "My Chart",
  "width": 800,
  "height": 400,
  "margin": { "top": 40, "right": 20, "bottom": 40, "left": 50 },
  "x_axis": { "label": "X Axis", "scale": "linear" },
  "y_axis": { "label": "Y Axis", "scale": "log" }
}
```

## License

MIT
