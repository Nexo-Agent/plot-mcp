# PlotMCP Server

PlotMCP is a powerful Model Context Protocol (MCP) server designed to enable LLMs to generate high-quality SVG charts from structured data. It leverages `fastmcp` for the server infrastructure and `matplotlib` for consistent, precise chart rendering.

## Key Features

- **Pure SVG Rendering**: Generates static SVG format with no external JavaScript dependencies. Safe, portable, and easy to embed.
- **Multiple Plot Types**: Supports Line, Scatter, Bar, Area, Histogram, Box, Heatmap, Contour, and Pie charts.
- **Flexible Configuration**: Full control over titles, dimensions, margins, and axis properties (linear, log, and symlog scales).
- **Output Management**: When `--output-dir` is configured, automatically saves generated charts and returns a specially formatted response that clients can parse to display the image:
  ````markdown
  ```local_image
  /path/to/chart.svg
  ```
  ````
  This format allows clients to easily detect and render the generated images.
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

## Output Format

The server supports two output modes depending on whether `--output-dir` is configured:

### Without `--output-dir` (Default)

Tools return a `PlotOutput` object containing the raw SVG content:

```json
{
  "svg": "<svg>...</svg>",
  "width": 800,
  "height": 400,
  "viewBox": "0 0 800 400"
}
```

### With `--output-dir` (Recommended)

Tools save the SVG to a file and return a specially formatted string:

````markdown
```local_image
/absolute/path/to/chart.svg
```
````

This format is designed to be easily parsed by clients. When your client receives a response containing this pattern, it should:

1. Detect the ` ```local_image` marker
2. Extract the file path
3. Load and display the image from that path

This approach keeps the response lightweight and allows clients to handle image rendering efficiently.

**See [`examples/local_image_format.py`](examples/local_image_format.py) for a complete demonstration of how this format works.**

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
