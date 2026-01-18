#!/usr/bin/env python3
"""
Example demonstrating the local_image output format.

This script shows how the PlotMCP server returns results in the special
local_image format when --output-dir is configured.
"""

import os
import tempfile
import json
from plot_mcp.models import LineData, LineSeries, LineConfig, PlotOutput
from plot_mcp.renderer import render_line
import plot_mcp.main as main_module

def main():
    # Create a temporary directory for outputs
    temp_dir = tempfile.mkdtemp()
    print(f"📁 Output directory: {temp_dir}\n")
    
    # Configure OUTPUT_DIR
    main_module.OUTPUT_DIR = temp_dir
    
    # Create sample data
    data = LineData(
        series=[
            LineSeries(
                name="Sales",
                x=[1, 2, 3, 4, 5],
                y=[10, 25, 15, 30, 20]
            )
        ]
    )
    
    config = LineConfig(
        title="Monthly Sales",
        width=800,
        height=400
    )
    
    # Render the chart
    print("🎨 Rendering chart...")
    output = render_line(data, config)
    
    # Process through save_svg_and_update_output
    result = main_module.save_svg_and_update_output(output, "line", config)
    
    print("✅ Chart generated!\n")
    print("📤 Server response:")
    print("-" * 60)
    print(result)
    print("-" * 60)
    print()
    
    # Show how a client would parse this
    print("🔍 Client parsing example:")
    print("1. Detect the ```local_image marker")
    print("2. Extract the file path")
    
    if isinstance(result, str) and "```local_image" in result:
        # Extract path from the formatted string
        lines = result.strip().split('\n')
        if len(lines) >= 2:
            file_path = lines[1]
            print(f"3. File path extracted: {file_path}")
            print(f"4. File exists: {os.path.exists(file_path)}")
            print(f"5. File size: {os.path.getsize(file_path)} bytes")
    
    print()
    print("💡 This format allows clients to:")
    print("   - Easily detect image responses")
    print("   - Extract file paths with simple string parsing")
    print("   - Load and display images efficiently")
    print("   - Keep response payloads lightweight")
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)
    print(f"\n🧹 Cleaned up temporary directory")

if __name__ == "__main__":
    main()
