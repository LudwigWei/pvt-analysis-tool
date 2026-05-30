# PVT Analysis Tool

## Overview
The PVT Analysis Tool is a commissioned project built for Reservoir Engineering workflows. Built with Streamlit, it calculates, visualizes, and interprets fluid properties (Pressure-Volume-Temperature correlations) using industry-standard empirical models.

## Core Analytical Features
- **Data processing and transformation:** Generates PVT datasets with Standing, Beggs-Robinson, Lee-Gonzalez, and Papay correlations.
- **Automated insight generation:** Classifies fluid types (for example Volatile Oil or Retrograde Gas) and provides technical interpretations of dominant drive mechanisms.
- **Interactive visualization:** Uses Plotly to render high-contrast charts for trends like oil FVF and gas Z-factor across pressure steps.
- **Modern, responsive UI:** Streamlit UI with custom CSS, bento-box layouts, and a dark industrial theme for readability.
- **Export and reporting:** Exports DataFrames to CSV and provides a print-ready reporting mode.

## Tech Stack
| Layer | Tools | Notes |
| --- | --- | --- |
| App framework | Streamlit | Web app runtime and UI layout |
| Language | Python 3.8+ | Core runtime |
| Data | Pandas, NumPy | Calculations and tabular assembly |
| Visualization | Plotly Graph Objects | Interactive charts |
| Styling | Custom CSS, HTML injection | Theme and layout control |

## Data Pipeline Architecture
| Stage | Inputs | Processing | Outputs | Files/Modules |
| --- | --- | --- | --- | --- |
| Parameter ingestion | API Gravity, temperature, solution GOR, gas specific gravity, bubble point pressure | Validate and normalize inputs | Cleaned inputs | app.py, components/inputs.py |
| Correlation engine | Cleaned inputs, pressure steps | Apply empirical models for viscosity, compressibility, and FVFs | Raw computed properties | pvt_correlations.py |
| Data assembly | Computed properties | Build structured DataFrame | PVT DataFrame | pvt_correlations.py |
| Rendering and interpretation | PVT DataFrame | Charting and insights | Charts, narrative analysis | components/charts.py, components/results.py |

## Prerequisites
- Python 3.8 or higher
- pip

## Installation and Setup
1. Clone the repository and move into the project directory:
   ```bash
   git clone https://github.com/yourusername/pvt-analysis-tool.git
   cd pvt-analysis-tool
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the app from the project root:
```bash
streamlit run app.py
```

The dashboard opens at http://localhost:8501.
