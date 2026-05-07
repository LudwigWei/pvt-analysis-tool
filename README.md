# PVT Analysis Tool

## Overview
The PVT Analysis Tool is a comprehensive, web-based dashboard designed for Reservoir Engineering applications. Built with Streamlit, this application allows engineers to calculate, visualize, and analyze fluid properties (Pressure-Volume-Temperature correlations) using industry-standard empirical models.

## Key Features
- **Industry-Standard Models:** Calculates properties using recognized correlations including Standing, Beggs-Robinson, Lee-Gonzalez, and Papay.
- **Flexible Data Input:** Enter reservoir parameters manually or upload bulk data via CSV.
- **Core Parameters Supported:** Handles essential inputs such as API Gravity, Temperature, Solution Gas-Oil Ratio (GOR), Gas Specific Gravity, and Bubble Point Pressure.
- **Fluid Classification:** Automatically analyzes and classifies fluid types based on input properties.
- **Detailed Property Tables:** Generates clear, tabulated data of calculated PVT properties across various pressure steps.
- **Interactive Visualization:** Features dynamic Plotly charts for visual analysis of fluid behavior and phase trends.
- **Interpretation Summary:** Provides automated technical insights and summaries based on the calculated properties.

## Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Navigate to the project directory:
   ```bash
   cd pvt-analysis-tool
   ```

2. (Optional but recommended) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install the required dependencies using `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To start the application locally, run the following command from the project root:

```bash
streamlit run app.py
```

Once the server initializes, your default web browser will automatically open the dashboard (typically accessible at `http://localhost:8501`).
