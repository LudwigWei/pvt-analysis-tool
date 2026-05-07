import streamlit as st

THEME = {
    "bg": "#0A0A0B",         # Deep Vercel Black
    "bg2": "#141415",        # Elevated Cards
    "bg3": "#1C1C1E",        # Hover/Active states
    "border": "#27272A",     # Soft borders
    "border_hover": "#3F3F46",
    "accent": "#3B82F6",     # Modern sleek blue
    "accent_glow": "rgba(59, 130, 246, 0.15)",
    "accent2": "#10B981",    # Emerald
    "accent3": "#F59E0B",    # Amber
    "accent4": "#EF4444",    # Rose
    "accent5": "#8B5CF6",    # Violet
    "text": "#FAFAFA",       # Crisp white
    "muted": "#A1A1AA",      # Soft gray for text
    "label": "#71717A"       # Deeper gray for labels
}

def apply_custom_css():
    css = f"""
    <style>
    /* Import Modern Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

    /* BASE TYPOGRAPHY */
    html, body, [class*="css"], .stApp, p, div, span, label, button {{ 
        font-family: 'Inter', sans-serif !important; 
    }}
    
    /* NUMBERS & TABLES USE MONOSPACE */
    input, table, th, td, .metric-value, .logo-icon {{
        font-family: 'JetBrains Mono', monospace !important;
    }}
    
    /* SCROLLBAR */
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: {THEME['border_hover']}; border-radius: 10px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: {THEME['muted']}; }}

    /* HIDE STREAMLIT NATIVE LOADING ELEMENTS */
    [data-testid="stAppSkeleton"],
    [data-testid="stSkeleton"],
    .stSkeleton,
    [data-testid="stStatusWidget"] {{
        display: none !important;
        visibility: hidden !important;
    }}

    /* APP BACKGROUND & LAYOUT */
    html, body, .stApp {{ background-color: {THEME['bg']} !important; color: {THEME['text']} !important; }}
    .block-container {{ 
        max-width: 1400px !important; 
        margin: 0 auto !important; 
        padding-top: 4.5rem !important; /* Adjusted slightly to preserve header clearance */
        padding-bottom: 2rem !important; 
        padding-left: 2.5rem !important; 
        padding-right: 2.5rem !important; 
    }}

    /* HIDE DEFAULT STREAMLIT ELEMENTS */
    header, [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="collapsedControl"], section[data-testid="stSidebar"] {{ display: none !important; }}

    /* MODERN GLASS HEADER */
    .fixed-header {{ 
        position: fixed; top: 0; left: 0; right: 0; width: 100vw; 
        background: rgba(10, 10, 11, 0.7); 
        backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); 
        border-bottom: 1px solid {THEME['border']}; 
        z-index: 99999; display: flex; justify-content: center; padding: 0.5rem 0 !important; 
    }}
    .header-inner {{ width: 100%; max-width: 1400px; padding: 0 2.5rem !important; display: flex; justify-content: space-between; align-items: center; }}
    .logo-group {{ display: flex; align-items: center; gap: 12px; }}
    .logo-icon {{ 
        width: 34px; height: 34px; background: linear-gradient(135deg, {THEME['bg2']}, {THEME['bg3']}); 
        border: 1px solid {THEME['border_hover']}; box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        border-radius: 8px; display: flex; align-items: center; justify-content: center; 
        font-weight: 500; color: {THEME['text']}; font-size: 13px; 
    }}
    .logo-text {{ font-size: 15px; font-weight: 600; color: {THEME['text']}; letter-spacing: -0.3px; }}
    .logo-sub {{ font-size: 12px; color: {THEME['muted']}; font-weight: 400; }}
    .header-badge {{ 
        font-size: 11px; font-weight: 500; color: {THEME['muted']}; background: {THEME['bg2']}; 
        border: 1px solid {THEME['border']}; padding: 4px 12px; border-radius: 20px; 
    }}

    /* MODERN BENTO CARDS */
    [data-testid="stVerticalBlockBorderWrapper"] {{ 
        background-color: {THEME['bg2']} !important; 
        border: 1px solid {THEME['border']} !important; 
        border-radius: 16px !important; 
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
        overflow: hidden !important; 
        transition: all 0.3s ease;
    }}
    [data-testid="stVerticalBlockBorderWrapper"]:hover {{ border-color: {THEME['border_hover']} !important; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05) !important; }}
    [data-testid="stVerticalBlockBorderWrapper"] > div[data-testid="stVerticalBlock"] {{ background-color: transparent !important; }}

    /* CARD HEADERS */
    .card-header {{ 
        margin: -1rem -1rem 1rem -1rem !important; 
        padding: 1rem 1.25rem !important; 
        border-bottom: 1px solid {THEME['border']} !important; 
        font-size: 12px !important; color: {THEME['text']} !important; 
        font-weight: 600 !important; letter-spacing: 0.02em !important; 
        display: flex !important; align-items: center !important; gap: 8px !important; 
        background-color: rgba(255,255,255,0.01) !important;
    }}
    
    /* INPUT FIELDS UX */
    div[data-testid="stMarkdownContainer"] p, [data-testid="stWidgetLabel"] p {{ 
        margin-bottom: 0 !important; 
        font-size: 13px !important; 
        line-height: 1.2 !important;
    }}
    
    [data-testid="column"] > div {{
        width: 100% !important;
    }}
    
    div[data-testid="stNumberInput"] {{ 
        margin-top: 4px !important; 
        margin-bottom: 0.75rem !important; 
        width: 100% !important;
    }}
    
    /* Ensure columns have a clean medium gap without squashing content */
    div[data-testid="stVerticalBlock"] > div[data-testid="stHorizontalBlock"] {{ gap: 1.5rem !important; }}
    
    /* ONLY hide the input instructions, NOT all <small> tags */
    div[data-testid="InputInstructions"] {{ display: none !important; }}
    
    div[data-baseweb="input"] > div, div[data-baseweb="base-input"] {{ 
        background-color: {THEME['bg']} !important; border: 1px solid {THEME['border']} !important; 
        border-radius: 8px !important; transition: all 0.2s ease; min-height: 38px !important;
        width: 100% !important;
    }}
    div[data-baseweb="input"] > div:focus-within {{ border-color: {THEME['accent']} !important; box-shadow: 0 0 0 2px {THEME['accent_glow']} !important; }}
    input[type="number"] {{ background-color: transparent !important; color: {THEME['text']} !important; font-size: 14px !important; padding: 4px 12px !important; width: 100% !important; box-sizing: border-box !important; -moz-appearance: textfield !important; }}
    
    /* Hide Streamlit's custom +/- buttons */
    [data-testid="stNumberInput"] button {{
        display: none !important;
    }}

    /* Hide native browser spin buttons just in case */
    input[type="number"]::-webkit-inner-spin-button, 
    input[type="number"]::-webkit-outer-spin-button {{
        -webkit-appearance: none !important;
        margin: 0 !important;
    }}

    /* BUTTONS (Export CSV) */
    [data-testid="stDownloadButton"] button,
    [data-testid="stDownloadButton"] button p {{
        font-family: 'Inter', sans-serif !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        color: {THEME['text']} !important;
        letter-spacing: 0.3px !important;
        margin: 0 !important;
        line-height: 1 !important;
    }}
    [data-testid="stDownloadButton"] button {{
        background-color: {THEME['bg2']} !important; 
        background-image: linear-gradient(180deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0) 100%) !important;
        border: 1px solid {THEME['border']} !important;
        padding: 0 14px !important;
        border-radius: 8px !important; 
        height: 36px !important; 
        min-height: 36px !important; 
        transition: all 0.2s ease !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05) !important;
    }}
    [data-testid="stDownloadButton"] button:hover {{ 
        border-color: {THEME['border_hover']} !important; 
        color: {THEME['text']} !important; 
        background-color: {THEME['bg2']} !important;
        background-image: linear-gradient(180deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.02) 100%) !important;
        
    }}

    /* TABS UX - MODERN SEGMENTED CONTROL */
    [data-testid="stTabs"] {{ gap: 0 !important; }}
    
    /* FILE UPLOADER HACK TO LOOK LIKE SIMPLE BUTTON */
    [data-testid="stFileUploaderDropzone"] {{
        padding: 0 !important;
        background: transparent !important;
        border: 0 !important;
        font-size: 0px !important;
    }}
    [data-testid="stFileUploaderDropzone"] svg, 
    [data-testid="stFileUploaderDropzone"] small {{
        display: none !important;
    }}
    [data-testid="stFileUploaderDropzone"] button {{
        width: 100% !important;
        border: 1px solid {THEME['border']} !important;
        background: transparent !important;
        border-radius: 5px !important;
        color: transparent !important;
        position: relative !important;
    }}
    [data-testid="stFileUploaderDropzone"] button::after {{
        content: "Upload CSV" !important;
        color: #A1A1AA !important;
        display: block !important;
        text-align: center !important;
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        width: 100% !important;
        font-size: 14px !important;
    }}
    
    [data-testid="stTabs"] div[role="tablist"] {{
        background-color: {THEME['bg']} !important;
        padding: 4px !important;
        border-radius: 10px !important;
        border: 1px solid {THEME['border']} !important;
        display: inline-flex !important;
        margin-bottom: 1.5rem !important;
        gap: 4px !important;
    }}
    
    [data-testid="stTabs"] button[data-baseweb="tab"] {{
        background-color: transparent !important;
        border: 1px solid transparent !important;
        color: {THEME['muted']} !important;
        padding: 6px 16px !important;
        font-weight: 500 !important;
        font-size: 13px !important;
        border-radius: 6px !important;
        transition: all 0.2s ease !important;
        margin: 0 !important;
    }}
    
    [data-testid="stTabs"] button[data-baseweb="tab"]:hover {{
        color: {THEME['text']} !important;
        background-color: rgba(255,255,255,0.03) !important;
    }}
    
    [data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] {{
        background-color: {THEME['bg2']} !important;
        color: {THEME['text']} !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
        border: 1px solid {THEME['border_hover']} !important;
    }}
    
    /* Hide the default animated bottom border */
    [data-testid="stTabs"] div[data-baseweb="tab-highlight"] {{ display: none !important; }}
    [data-testid="stTabs"] div[data-baseweb="tab-border"] {{ display: none !important; }}

    /* MODERN TABLES */
    table {{ width: 100%; border-collapse: separate; border-spacing: 0; font-size: 13px; }}
    thead th {{ text-align: left; padding: 12px; font-size: 11px; color: {THEME['muted']}; border-bottom: 1px solid {THEME['border']}; font-family: 'Inter', sans-serif; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; }}
    tbody td {{ padding: 10px 12px; border-bottom: 1px solid {THEME['border']}; color: {THEME['muted']}; transition: background 0.2s; }}
    tbody tr:first-child td {{ color: {THEME['text']}; font-weight: 500; background: linear-gradient(90deg, rgba(59,130,246,0.05) 0%, transparent 100%); }}
    tbody tr:hover td {{ background: {THEME['bg3']}; color: {THEME['text']}; }} 
    
    [data-testid="stPlotlyChart"] {{ margin-bottom: 0.5rem !important; }}

    /* --- PRINT STYLES (WHITE PAPER MODE) --- */
    @media print {{
        * {{
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }}

        /* 1. Hide Everything Except Results */
        header, [data-testid="stHeader"], [data-testid="stSidebar"], section[data-testid="stSidebar"],
        .fixed-header, [data-testid="stToolbar"], [data-testid="collapsedControl"],
        [role="tablist"], button, .stButton, [data-testid="stFileUploader"], 
        [data-testid="stDownloadButton"], [data-testid="stFileUploaderDropzone"], small {{
            display: none !important;
        }}

        /* Hide the entire left column (where inputs and models are) */
        [data-testid="column"]:has([data-testid="stNumberInput"]),
        [data-testid="column"]:has(div:contains('Reservoir Parameters')),
        [data-testid="column"]:has(div:contains('Active Models')) {{
            display: none !important;
        }}

        /* Hide Property Table */
        [data-baseweb="tab-panel"]:nth-of-type(1), table, thead, tbody, tr, th, td {{
            display: none !important;
        }}

        /* 2. Fix Structural Overlap (Full-Width Mode) */
        [data-testid="column"], [data-testid="stHorizontalBlock"] {{
            width: 100% !important;
            flex: none !important;
            max-width: none !important;
            min-width: 100% !important;
            display: block !important;
        }}

        /* Force All Tabs Open */
        [data-baseweb="tab-panel"] {{
            display: block !important;
            opacity: 1 !important;
            visibility: visible !important;
            height: auto !important;
            position: relative !important;
        }}

        /* 3. Professional Formatting */
        /* Metrics Grid */
        div[data-testid="stMarkdownContainer"] > div[style*="display: grid"] {{
            display: grid !important;
            grid-template-columns: 1fr 1fr 1fr !important;
            gap: 12px !important;
        }}

        /* Charts */
        [data-testid="stPlotlyChart"] {{
            width: 100% !important;
            page-break-inside: avoid !important;
            break-inside: avoid !important;
        }}

        /* Interpretation */
        div[data-testid="stMarkdownContainer"] > div {{
            page-break-inside: avoid !important;
            break-inside: avoid !important;
        }}

        [data-testid="stVerticalBlockBorderWrapper"] {{
            box-shadow: none !important;
            border: 1px solid #E5E7EB !important;
            page-break-inside: avoid !important;
            break-inside: avoid !important;
        }}

        [data-baseweb="tab-panel"]:nth-of-type(3) {{
            margin-top: 30px !important;
        }}

        /* 4. Ink-Friendly Colors */
        html, body, .stApp, .block-container, [data-testid="stVerticalBlockBorderWrapper"], .card-header {{
            background-color: #FFFFFF !important;
            background: #FFFFFF !important;
            color: #000000 !important;
            box-shadow: none !important;
        }}
        
        p, h1, h2, h3, h4, h5, h6, span, div, label, .metric-value, .input-unit {{
            color: #000000 !important;
        }}

        /* Remove dark-mode gradients from banner and cards */
        div[style*="linear-gradient"] {{
            background: #FFFFFF !important;
            background-image: none !important;
            border: 1px solid #E5E7EB !important;
            border-left-width: 5px !important;
            box-shadow: none !important;
        }}
        
        /* Metric cards background reset */
        div[style*="background: #141415"] {{
            background: #FFFFFF !important;
            background-color: #FFFFFF !important;
            border: 1px solid #E5E7EB !important;
        }}

        /* Maximize print layout width */
        .block-container {{
            max-width: 100% !important;
            padding: 0 !important;
            margin: 0 !important;
        }}
    }}

    /* PREMIUM PRIMARY BUTTON (Run Analysis) */
    button[kind="primary"], [data-testid="baseButton-primary"] {{
        background: linear-gradient(180deg, #22D3EE 0%, #06B6D4 100%) !important;
        border: 1px solid #0891B2 !important;
        color: #050505 !important;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.2), 0 4px 14px rgba(6, 182, 212, 0.2) !important;
        font-weight: 600 !important;
        text-align: center !important;
        transition: all 0.2s ease !important;
    }}
    button[kind="primary"]:hover, [data-testid="baseButton-primary"]:hover {{
        background: linear-gradient(180deg, #38BDF8 0%, #0891B2 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.3), 0 6px 20px rgba(6, 182, 212, 0.35) !important;
    }}
    button[kind="primary"]:active, [data-testid="baseButton-primary"]:active {{
        transform: translateY(1px) !important;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.05), 0 2px 8px rgba(6, 182, 212, 0.15) !important;
    }}

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)