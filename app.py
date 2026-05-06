import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
import pvt_correlations as pvt

# ==========================================
# 1. CONFIGURATION & THEME
# ==========================================

THEME = {
    "bg": "#0d0f14",         # Overall App Background (Darkest)
    "bg2": "#13161e",        # Inset Wells: Inputs, Metric Cards, Correlation Boxes
    "bg3": "#1a1e28",        # Main Cards: Left Panel, Results Panel, Fluid Banner
    "border": "#252a38",
    "accent": "#3b82f6",     
    "accent2": "#10b981",    
    "accent3": "#f59e0b",    
    "accent4": "#ef4444",    
    "accent5": "#8b5cf6",    
    "text": "#e2e8f0",
    "muted": "#64748b",
    "label": "#94a3b8"
}

def init_session_state():
    if 'analysis_run' not in st.session_state:
        st.session_state.analysis_run = False
    if 'saved_inputs' not in st.session_state:
        st.session_state.saved_inputs = {}

# ==========================================
# 2. CSS STYLING
# ==========================================

def apply_custom_css():
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&display=swap');

    /* UNIVERSAL FONT */
    html, body, [class*="css"], .stApp, p, div, span, label, input, button, table, th, td {{ 
        font-family: 'IBM Plex Mono', monospace !important; 
    }}
    
    /* APP BACKGROUND */
    html, body, .stApp {{
        background-color: {THEME['bg']} !important; 
    }}
    
    /* HIDE STREAMLIT HEADER & TOOLBAR  */
    header {{ display: none !important; visibility: hidden !important; }}
    [data-testid="stHeader"] {{ display: none !important; }}
    [data-testid="stToolbar"] {{ display: none !important; }}
    
    [data-testid="collapsedControl"], section[data-testid="stSidebar"] {{ display: none !important; }}
    .block-container {{ max-width: 1300px !important; margin: 0 auto !important; padding-top: 6.5rem !important; padding-bottom: 4rem !important; }}

    /* FIXED HEADER */
    .fixed-header {{ position: fixed; top: 0; left: 0; right: 0; width: 100vw; background-color: {THEME['bg']}; border-bottom: 1px solid {THEME['border']}; z-index: 99999; display: flex; justify-content: center; padding: 1rem 0; }}
    .header-inner {{ width: 100%; max-width: 100%; padding: 0 2rem; display: flex; justify-content: space-between; align-items: center; }}
    .logo-group {{ display: flex; align-items: center; gap: 12px; }}
    .logo-icon {{ width: 32px; height: 32px; background: {THEME['accent']}; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-family: 'IBM Plex Mono', monospace; font-size: 12px; font-weight: 500; color: #fff; letter-spacing: -0.5px; }}
    .logo-text {{ font-size: 15px; font-weight: 500; color: {THEME['text']}; line-height: 1.2; }}
    .logo-sub {{ font-size: 11px; color: {THEME['muted']}; font-family: 'IBM Plex Mono', monospace; }}
    .header-badge {{ font-size: 11px; font-family: 'IBM Plex Mono', monospace; color: {THEME['accent2']}; background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.2); padding: 4px 10px; border-radius: 4px; }}

    /*  MAIN CARDS */
    [data-testid="stVerticalBlockBorderWrapper"] {{ 
        background-color: {THEME['bg3']} !important; 
        border: 1px solid {THEME['border']} !important; 
        border-radius: 8px !important; 
        overflow: hidden !important; 
    }}
    
    [data-testid="stVerticalBlockBorderWrapper"] > div[data-testid="stVerticalBlock"] {{
        background-color: transparent !important;
    }}

    .card-header {{ 
        margin: -1rem -1rem 1.25rem -1rem !important; 
        padding: 0.875rem 1.25rem !important; 
        border-bottom: 1px solid {THEME['border']} !important; 
        font-size: 11px !important; 
        font-family: 'IBM Plex Mono', monospace !important; 
        color: {THEME['muted']} !important; 
        letter-spacing: 0.08em !important; 
        text-transform: uppercase !important; 
        display: flex !important; 
        align-items: center !important; 
        gap: 8px !important; 
        background-color: {THEME['bg3']} !important; 
        border-radius: 7px 7px 0 0 !important; 
    }}
    .card-header::before {{ content: ''; width: 6px; height: 6px; border-radius: 50%; background: {THEME['accent']}; display: inline-block; }}
    
    /* INPUT FIELDS */
    .stNumberInput > label {{ font-size: 11px !important; font-family: 'IBM Plex Mono', monospace !important; color: {THEME['label']} !important; letter-spacing: 0.02em !important; }}
    div[data-testid="stNumberInput"] {{ margin-bottom: 0 !important; }}
    
    /* FIX: Hide the overlapping "Press Enter to apply" text completely */
    div[data-testid="InputInstructions"], small {{ display: none !important; }}
    
    div[data-baseweb="input"] > div,
    div[data-baseweb="base-input"] {{
        background-color: {THEME['bg2']} !important;
        border: 1px solid {THEME['border']} !important;
        border-radius: 6px !important;
    }}
    input[type="number"] {{
        background-color: {THEME['bg2']} !important;
        color: {THEME['text']} !important;
    }}
    div[data-testid="stNumberInputStepUp"], 
    div[data-testid="stNumberInputStepDown"],
    button[aria-label="Step Up"],
    button[aria-label="Step Down"] {{
        background-color: {THEME['bg2']} !important;
        color: {THEME['muted']} !important;
    }}
    
    .input-unit {{ font-size: 10px; color: {THEME['muted']}; font-family: 'IBM Plex Mono', monospace; margin-top: -0.75rem; margin-bottom: 1rem; }}

    /* BUTTONS & TABS */
    .stButton > button[kind="primary"] {{ 
        background-color: {THEME['accent']} !important; 
        border-color: {THEME['accent']} !important; 
        color: #fff !important; 
        transition: opacity 0.15s, transform 0.1s; 
    }}
    .stButton > button[kind="primary"]:hover {{ opacity: 0.88; transform: scale(0.99); }}
    
    [data-testid="stDownloadButton"] button {{
        background-color: transparent !important;
        border: 1px solid {THEME['border']} !important;
        color: {THEME['label']} !important;
        font-size: 12px !important;
        padding: 0 14px !important;
        border-radius: 5px !important;
        height: 35px !important;
        min-height: 35px !important;
        transition: all 0.15s !important;
    }}
    [data-testid="stDownloadButton"] button:hover {{
        border-color: {THEME['accent']} !important;
        color: {THEME['accent']} !important;
    }}
    
    div[data-baseweb="tab-list"] {{ gap: 8px; margin-bottom: 1rem; background-color: transparent !important; }}
    div[data-baseweb="tab"] {{ background-color: transparent !important; border: 1px solid {THEME['border']} !important; border-radius: 5px !important; color: {THEME['muted']} !important; padding: 6px 14px !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 12px !important; height: auto !important; }}
    div[aria-selected="true"] {{ background-color: {THEME['accent']} !important; border-color: {THEME['accent']} !important; color: #fff !important; }}
    div[data-baseweb="tab-highlight"], div[data-baseweb="tab-border"] {{ display: none !important; }}

    /* TABLES & PLOTLY */
    table {{ width: 100%; border-collapse: collapse; font-family: 'IBM Plex Mono', monospace; font-size: 12px; background: transparent; }}
    thead th {{ text-align: left; padding: 8px 10px; font-size: 10px; color: {THEME['muted']}; border-bottom: 1px solid {THEME['border']}; white-space: nowrap; font-weight: 400; letter-spacing: 0.04em; }}
    tbody td {{ padding: 7px 10px; border-bottom: 1px solid rgba(37,42,56,0.6); color: {THEME['text']}; white-space: nowrap; }}
    tbody tr:first-child td {{ color: {THEME['accent']}; font-weight: 500; }}
    tbody tr:hover td {{ background: {THEME['bg2']}; }} 
    [data-testid="stPlotlyChart"] {{ margin-bottom: 0.5rem !important; }}
    [data-testid="stPlotlyChart"] > div > div {{ border-radius: 8px !important; overflow: hidden; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ==========================================
# 3. UI RENDER FUNCTIONS
# ==========================================

def render_header():
    st.markdown(f"""
    <div class="fixed-header">
        <div class="header-inner">
            <div class="logo-group">
                <div class="logo-icon">PVT</div>
                <div>
                    <div class="logo-text">PVT Analysis Tool</div>
                    <div class="logo-sub">Reservoir Engineering · Phase 2</div>
                </div>
            </div>
            <div class="header-badge">Standing · Beggs-Robinson · Papay · LGE</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_input_panel():
    with st.container(border=True):
        st.markdown('<div class="card-header">Fluid & Reservoir Data</div>', unsafe_allow_html=True)

        api = st.number_input("API Gravity", min_value=1.0, value=35.0, step=0.1, format="%g")
        st.markdown('<div class="input-unit">°API</div>', unsafe_allow_html=True)

        gg = st.number_input("Gas Specific Gravity", min_value=0.5, value=0.65, step=0.01)
        st.markdown('<div class="input-unit">air = 1.0</div>', unsafe_allow_html=True)

        temp = st.number_input("Reservoir Temperature", min_value=50, value=180, step=1)
        st.markdown(f'<div class="input-unit">°F</div><hr style="border-color:{THEME["border"]}; margin:0.5rem 0 1rem;">', unsafe_allow_html=True)

        pb = st.number_input("Bubble Point Pressure (Pb)", min_value=100, value=2500, step=1)
        st.markdown('<div class="input-unit">psia</div>', unsafe_allow_html=True)

        rs_pb = st.number_input("Solution GOR at Pb", min_value=10, value=650, step=1)
        st.markdown('<div class="input-unit">scf/STB</div>', unsafe_allow_html=True)

        gor = st.number_input("Producing GOR", min_value=0, value=650, step=1)
        st.markdown('<div class="input-unit">scf/STB — classification</div><br>', unsafe_allow_html=True)

        if st.button("▶ Run PVT Analysis", type="primary", use_container_width=True):
            st.session_state.analysis_run = True
            st.session_state.saved_inputs = {"api": api, "gg": gg, "temp": temp, "pb": pb, "rs_pb": rs_pb, "gor": gor}

def render_correlations_panel():
    with st.container(border=True):
        st.markdown('<div class="card-header">Correlations Used</div>', unsafe_allow_html=True)
        html_str = f"""
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 8px;'>
            <div style='background:{THEME['bg2']}; border:1px solid {THEME['border']}; padding:8px 10px; border-radius:6px;'>
                <div style='font-size:10px; color:{THEME['muted']};'>Rs, Bo, Pb, co</div>
                <div style='font-size:10px; color:{THEME['text']}; font-weight:500; margin-top:2px;'>Standing's</div>
            </div>
            <div style='background:{THEME['bg2']}; border:1px solid {THEME['border']}; padding:8px 10px; border-radius:6px;'>
                <div style='font-size:10px; color:{THEME['muted']};'>Oil Viscosity</div>
                <div style='font-size:10px; color:{THEME['text']}; font-weight:500; margin-top:2px;'>Beggs-Robinson</div>
            </div>
            <div style='background:{THEME['bg2']}; border:1px solid {THEME['border']}; padding:8px 10px; border-radius:6px;'>
                <div style='font-size:10px; color:{THEME['muted']};'>Z-factor</div>
                <div style='font-size:10px; color:{THEME['text']}; font-weight:500; margin-top:2px;'>Papay</div>
            </div>
            <div style='background:{THEME['bg2']}; border:1px solid {THEME['border']}; padding:8px 10px; border-radius:6px;'>
                <div style='font-size:10px; color:{THEME['muted']};'>Gas Viscosity</div>
                <div style='font-size:10px; color:{THEME['text']}; font-weight:500; margin-top:2px;'>Lee-Gonzalez-Eakin</div>
            </div>
            <div style='background:{THEME['bg2']}; border:1px solid {THEME['border']}; padding:8px 10px; border-radius:6px;'>
                <div style='font-size:10px; color:{THEME['muted']};'>Pseudo-critical</div>
                <div style='font-size:10px; color:{THEME['text']}; font-weight:500; margin-top:2px;'>Standing's</div>
            </div>
            <div style='background:{THEME['bg2']}; border:1px solid {THEME['border']}; padding:8px 10px; border-radius:6px;'>
                <div style='font-size:10px; color:{THEME['muted']};'>Gas FVF</div>
                <div style='font-size:10px; color:{THEME['text']}; font-weight:500; margin-top:2px;'>Real Gas Law</div>
            </div>
        </div>
        """
        st.markdown("".join(html_str.split('\n')), unsafe_allow_html=True)

# ==========================================
# 4. CHARTING HELPERS
# ==========================================

def hex_to_rgba(hex_color, alpha=0.15):
    h = hex_color.lstrip('#')
    return f'rgba({int(h[0:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)},{alpha})'

def render_area_chart(x, y, color, title_label):
    y_min, y_max = min(y), max(y)
    y_pad = (y_max - y_min) * 0.12 if y_max != y_min else abs(y_max) * 0.1 or 0.1
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y, mode='lines+markers',
        line=dict(color=color, width=1.8), marker=dict(size=6.0, color=color),
        fill='tozeroy', fillcolor=hex_to_rgba(color, 0.18)
    ))
    
    fig.update_layout(
        paper_bgcolor=THEME['bg2'], plot_bgcolor=THEME['bg2'],
        font=dict(family='IBM Plex Mono', size=9, color=THEME['muted']),
        margin=dict(l=44, r=12, t=36, b=32), height=180,
        title=dict(text=title_label, font=dict(size=9, color=THEME['muted']), x=0.01, y=0.92),
        xaxis=dict(autorange='reversed', showgrid=True, gridcolor='rgba(255,255,255,0.04)', linecolor='rgba(255,255,255,0.08)'),
        yaxis=dict(range=[max(0, y_min - y_pad), y_max + y_pad], showgrid=True, gridcolor='rgba(255,255,255,0.04)', linecolor='rgba(255,255,255,0.08)'),
        showlegend=False, hovermode='x unified',
        
        # 🔥 FIX: Smoothes the line transition instead of a hard flash 🔥
        uirevision='constant',       
        transition=dict(duration=500, easing="cubic-in-out")
    )
    # Passed theme=None to prevent Streamlit from overriding our custom Plotly transition settings
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}, theme=None)

# ==========================================
# 5. RESULTS VIEW BUILDERS
# ==========================================

def build_metric_card(label, value, unit, color):
    return f"<div style='background: {THEME['bg2']}; border: 1px solid {THEME['border']}; border-radius: 8px; padding: 1rem;'><div style='font-size: 10px; font-family: monospace; color: {THEME['muted']}; margin-bottom: 6px;'>{label}</div><div style='font-size: 20px; font-weight: 500; font-family: monospace; color: {color}; line-height: 1;'>{value}</div><div style='font-size: 10px; color: {THEME['muted']}; font-family: monospace; margin-top: 4px;'>{unit}</div></div>"

def render_results(inputs):
    fluid = pvt.classify_fluid(inputs['api'], inputs['gor'])
    
    fluid_colors = {
        'Dry Gas': THEME['accent'], 'Wet Gas': THEME['accent2'],
        'Gas Condensate / Retrograde Gas': THEME['accent3'],
        'Near-Critical / Volatile Oil': '#f97316',
        'Black Oil — Light Crude': THEME['accent'],
        'Black Oil — Medium Crude': THEME['accent5'],
        'Heavy Oil': THEME['accent4']
    }
    f_color = fluid_colors.get(fluid['name'], THEME['accent'])
    
    df = pvt.generate_pvt_table(inputs['api'], inputs['gg'], inputs['temp'], inputs['pb'], inputs['rs_pb'], steps=10)
    
    t_rankine = inputs['temp'] + 460
    tpc, ppc = pvt.calc_pseudo(inputs['gg'])
    bo_pb = pvt.calc_bo(inputs['api'], inputs['gg'], inputs['rs_pb'], t_rankine)
    muo_pb = pvt.calc_muo(inputs['api'], t_rankine, inputs['rs_pb'])
    z_pb = pvt.calc_z(inputs['pb'] / ppc, t_rankine / tpc)
    bg_pb = pvt.calc_bg(t_rankine, inputs['pb'], z_pb)
    mug_pb = pvt.calc_mug(t_rankine, inputs['pb'], inputs['gg'], z_pb)
    co_pb = pvt.calc_co(inputs['api'], inputs['gg'], inputs['rs_pb'], t_rankine, inputs['pb'], bo_pb)

    banner_html = f"<div style='background: {THEME['bg3']}; border: 1px solid {f_color}44; border-radius: 8px; padding: 1.25rem; margin-bottom: 1.5rem;'><div style='font-size: 10px; font-family: monospace; color: {THEME['muted']}; margin-bottom: 6px;'>Fluid Classification</div><div style='font-size: 18px; font-weight: 500; color: {f_color}; margin-bottom: 4px;'>{fluid['name']}</div><div style='font-size: 12px; color: {THEME['muted']};'>{fluid['desc']}</div></div>"
    st.markdown(banner_html, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown('<div class="card-header">RESULTS</div>', unsafe_allow_html=True)
        
        metrics_html = f"<div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 1.5rem;'>{build_metric_card('Bo at Pb', f'{bo_pb:.4f}', 'RB/STB', THEME['accent'])}{build_metric_card('μo at Pb', f'{muo_pb:.3f}', 'cp', THEME['accent3'])}{build_metric_card('Z at Pb', f'{z_pb:.4f}', 'dimensionless', THEME['accent2'])}{build_metric_card('Bg at Pb', f'{bg_pb:.5f}', 'RB/Mscf', THEME['accent2'])}{build_metric_card('μg at Pb', f'{mug_pb:.5f}', 'cp', THEME['accent5'])}{build_metric_card('co at Pb', f'{co_pb:.2e}', 'psi⁻¹', THEME['accent4'])}</div>"
        st.markdown(metrics_html, unsafe_allow_html=True)

        # Action Buttons Aligned Properly
        btn_col1, btn_col2, _ = st.columns([1.5, 1.5, 7])
        with btn_col1:
            st.download_button("⬇ Export CSV", df.to_csv(index=False).encode('utf-8'), "pvt.csv", "text/csv", use_container_width=True)
        with btn_col2:
            
            # Formatted exactly to match the heights and borders of Streamlit's download button
            print_btn_style = f"background:transparent; border:1px solid {THEME['border']}; color:{THEME['label']}; padding:0 14px; border-radius:5px; cursor:pointer; width:100%; font-family:'IBM Plex Mono', monospace; font-size:12px; height:35px; line-height:33px; transition:all 0.15s;"
            hover_script = f"onmouseover=\"this.style.borderColor='{THEME['accent']}'; this.style.color='{THEME['accent']}';\" onmouseout=\"this.style.borderColor='{THEME['border']}'; this.style.color='{THEME['label']}';\""
            
            components.html(f"<button onclick='window.parent.print()' style=\"{print_btn_style}\" {hover_script}>⎙ Print</button>", height=35)

        tab1, tab2, tab3 = st.tabs(["Property Table", "Charts", "Interpretation"])

        with tab1:
            rows = "".join([f"<tr><td>{r['P (psia)']:.0f}</td><td>{r['Rs (scf/STB)']:.2f}</td><td>{r['Bo (RB/STB)']:.5f}</td><td>{r['muo (cp)']:.4f}</td><td>{r['co (psi-1)']}</td><td>{r['Z-factor']:.4f}</td><td>{r['Bg (RB/Mscf)']:.5f}</td><td>{r['mug (cp)']:.5f}</td></tr>" for _, r in df.iterrows()])
            table_html = f"<table><thead><tr><th>P (psia)</th><th>Rs (scf/STB)</th><th>Bo (RB/STB)</th><th>μo (cp)</th><th>co (psi⁻¹)</th><th>Z-factor</th><th>Bg (RB/Mscf)</th><th>μg (cp)</th></tr></thead><tbody>{rows}</tbody></table>"
            st.markdown(table_html, unsafe_allow_html=True)

        with tab2:
            pressures = df["P (psia)"].tolist()
            tc1, tc2 = st.columns(2, gap="small")
            with tc1:
                render_area_chart(pressures, df["Rs (scf/STB)"].tolist(), THEME['accent'], 'SOLUTION GOR (Rs) vs PRESSURE')
                render_area_chart(pressures, df["muo (cp)"].tolist(), THEME['accent3'], 'OIL VISCOSITY (μo) vs PRESSURE')
                render_area_chart(pressures, df["Z-factor"].tolist(), '#f97316', 'Z-FACTOR vs PRESSURE')
            with tc2:
                render_area_chart(pressures, df["Bo (RB/STB)"].tolist(), THEME['accent4'], 'OIL FVF (Bo) vs PRESSURE')
                render_area_chart(pressures, df["Bg (RB/Mscf)"].tolist(), THEME['accent2'], 'GAS FVF (Bg) vs PRESSURE')
                render_area_chart(pressures, df["mug (cp)"].tolist(), THEME['accent5'], 'GAS VISCOSITY (μg) vs PRESSURE')

        with tab3:
            Rs_min = f"{df['Rs (scf/STB)'].iloc[-1]:.1f}"
            Bo_min = f"{df['Bo (RB/STB)'].iloc[-1]:.4f}"
            muo_max = f"{df['muo (cp)'].max():.4f}"
            Bg_max = f"{df['Bg (RB/Mscf)'].iloc[-1]:.5f}"
            
            drive = "Solution gas drive is the dominant production mechanism. As reservoir pressure drops below Pb, dissolved gas expands and drives oil to the wellbore. Expect increasing GOR over time." if inputs['gor'] < 3300 else "Gas expansion drive is dominant. The system behaves as a gas or gas-condensate reservoir. Monitor condensate drop-out carefully near dew point."
            gravity = "Gravity drainage may also contribute due to the light oil (API > 35°). " if inputs['api'] > 35 else "Water influx from a connected aquifer could supplement drive energy if present. "

            interp_html = f"<div style='display: flex; flex-direction: column; gap: 12px; padding: 1rem 0;'><div style='display: flex; gap: 12px;'><div style='width:8px; height:8px; border-radius:50%; margin-top:6px; flex-shrink:0; background:{THEME['accent']};'></div><div style='font-size:13px; color:{THEME['label']};'><strong>Solution GOR (Rs)</strong> declines from <strong>{inputs['rs_pb']:.0f}</strong> → <strong>{Rs_min}</strong> scf/STB as pressure falls below bubble point. Dissolved gas evolves out of solution, reducing the gas available to drive production.</div></div><div style='display: flex; gap: 12px;'><div style='width:8px; height:8px; border-radius:50%; margin-top:6px; flex-shrink:0; background:{THEME['accent4']};'></div><div style='font-size:13px; color:{THEME['label']};'><strong>Oil FVF (Bo)</strong> decreases from <strong>{bo_pb:.4f}</strong> → <strong>{Bo_min}</strong> RB/STB. Shrinkage occurs as gas liberation reduces the volume of live oil in the reservoir relative to stock-tank conditions.</div></div><div style='display: flex; gap: 12px;'><div style='width:8px; height:8px; border-radius:50%; margin-top:6px; flex-shrink:0; background:{THEME['accent3']};'></div><div style='font-size:13px; color:{THEME['label']};'><strong>Oil viscosity (μo)</strong> increases to <strong>{muo_max}</strong> cp at the lowest pressure step. As lighter components flash off, the remaining oil becomes heavier and harder to produce — expect declining productivity index.</div></div><div style='display: flex; gap: 12px;'><div style='width:8px; height:8px; border-radius:50%; margin-top:6px; flex-shrink:0; background:{THEME['accent2']};'></div><div style='font-size:13px; color:{THEME['label']};'><strong>Gas FVF (Bg)</strong> rises to <strong>{Bg_max}</strong> RB/Mscf at low pressure. Liberated free gas expands significantly. Managing the gas-oil ratio (GOR) at surface becomes critical during late-stage depletion.</div></div><div style='display: flex; gap: 12px;'><div style='width:8px; height:8px; border-radius:50%; margin-top:6px; flex-shrink:0; background:#f97316;'></div><div style='font-size:13px; color:{THEME['label']};'><strong>Z-factor</strong> quantifies deviation from ideal gas behavior. Values below 1.0 reflect intermolecular attraction; values above 1.0 indicate repulsion at higher compression states. Use with Bg for accurate gas reserve estimation.</div></div><div style='display: flex; gap: 12px;'><div style='width:8px; height:8px; border-radius:50%; margin-top:6px; flex-shrink:0; background:{THEME['accent5']};'></div><div style='font-size:13px; color:{THEME['label']};'><strong>Drive mechanism:</strong> {drive} {gravity}</div></div></div>"
            st.markdown(interp_html, unsafe_allow_html=True)

def render_empty_state():
    with st.container(border=True):
        st.markdown('<div class="card-header">RESULTS</div>', unsafe_allow_html=True)
        st.markdown(f"""<div style="text-align:center; padding:6rem 2rem; color:{THEME['muted']};"><div style="font-size:48px; opacity:0.3; margin-bottom: 1.5rem;">⬡</div><div style="font-family:'IBM Plex Mono',monospace; font-size:13px;">Enter reservoir data and click Run to begin analysis.</div></div>""", unsafe_allow_html=True)

# ==========================================
# 6. MAIN APP EXECUTION
# ==========================================

def main():
    st.set_page_config(page_title="PVT Analysis Tool", layout="wide", initial_sidebar_state="collapsed")
    
    init_session_state()
    apply_custom_css()
    render_header()

    left_col, right_col = st.columns([1, 2.4], gap="medium")

    with left_col:
        render_input_panel()
        render_correlations_panel()

    with right_col:
        if st.session_state.analysis_run and 'saved_inputs' in st.session_state and st.session_state.saved_inputs:
            render_results(st.session_state.saved_inputs)
        else:
            render_empty_state()

if __name__ == "__main__":
    main()