import streamlit as st
import streamlit.components.v1 as components
import pvt_correlations as pvt
from utils.theme import THEME
from components.charts import render_area_chart

def build_metric_card(label, value, unit, color):
    return f"<div style='background: {THEME['bg2']}; border: 1px solid {THEME['border']}; border-radius: 8px; padding: 12px 16px;'><div style='font-size: 11px; font-family: monospace; color: {THEME['muted']}; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.05em;'>{label}</div><div style='display: flex; align-items: baseline; gap: 6px;'><div style='font-size: 26px; font-weight: 600; font-family: monospace; color: {color}; line-height: 1;'>{value}</div><div style='font-size: 12px; color: {THEME['muted']}; font-weight: 400; font-family: monospace;'>{unit}</div></div></div>"

def render_results(inputs):
    fluid = pvt.classify_fluid(inputs['api'], inputs['gor'])
    
    # Define colors for each fluid type
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
    
    # Calculate key parameters at bubble point for banner and metrics
    t_rankine = inputs['temp'] + 460
    tpc, ppc = pvt.calc_pseudo(inputs['gg'])
    bo_pb = pvt.calc_bo(inputs['api'], inputs['gg'], inputs['rs_pb'], t_rankine)
    muo_pb = pvt.calc_muo(inputs['api'], t_rankine, inputs['rs_pb'])
    z_pb = pvt.calc_z(inputs['pb'] / ppc, t_rankine / tpc)
    bg_pb = pvt.calc_bg(t_rankine, inputs['pb'], z_pb)
    mug_pb = pvt.calc_mug(t_rankine, inputs['pb'], inputs['gg'], z_pb)
    co_pb = pvt.calc_co(inputs['api'], inputs['gg'], inputs['rs_pb'], t_rankine, inputs['pb'], bo_pb)

    # Render banner with fluid classification
    banner_html = f"""
    <div style='background: linear-gradient(90deg, {f_color}1A 0%, {THEME['bg2']} 100%); border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; border-left: 5px solid {f_color}; box-shadow: 0 4px 15px rgba(0,0,0,0.1), inset 0 1px 0 rgba(255,255,255,0.02);'>
        <div style='font-size: 11px; font-family: monospace; color: {THEME['muted']}; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600;'>Fluid Classification</div>
        <div style='font-size: 26px; font-weight: 700; color: {f_color}; margin-bottom: 8px; text-shadow: 0 0 16px {f_color}4D; line-height: 1.2;'>{fluid['name']}</div>
        <div style='font-size: 14px; color: {THEME['text']}; line-height: 1.5; font-weight: 400;'>{fluid['desc']}</div>
    </div>
    """
    st.markdown(banner_html, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown('<div class="card-header">RESULTS</div>', unsafe_allow_html=True)
        
        metrics_html = f"<div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 1.5rem;'>{build_metric_card('Bo at Pb', f'{bo_pb:.4f}', 'RB/STB', THEME['accent'])}{build_metric_card('μo at Pb', f'{muo_pb:.3f}', 'cp', THEME['accent3'])}{build_metric_card('Z at Pb', f'{z_pb:.4f}', 'dimensionless', THEME['accent2'])}{build_metric_card('Bg at Pb', f'{bg_pb:.5f}', 'RB/Mscf', THEME['accent2'])}{build_metric_card('μg at Pb', f'{mug_pb:.5f}', 'cp', THEME['accent5'])}{build_metric_card('co at Pb', f'{co_pb:.2e}', 'psi⁻¹', THEME['accent4'])}</div>"
        st.markdown(metrics_html, unsafe_allow_html=True)

        # TABS
        tab1, tab2, tab3 = st.tabs(["Property Table", "Charts", "Interpretation"])

        with tab1:
            rows = "".join([f"<tr><td>{r['P (psia)']:.0f}</td><td>{r['Rs (scf/STB)']:.2f}</td><td>{r['Bo (RB/STB)']:.5f}</td><td>{r['muo (cp)']:.4f}</td><td>{r['co (psi-1)']}</td><td>{r['Z-factor']:.4f}</td><td>{r['Bg (RB/Mscf)']:.5f}</td><td>{r['mug (cp)']:.5f}</td></tr>" for _, r in df.iterrows()])
            table_html = f"<table><thead><tr><th>P (psia)</th><th>Rs (scf/STB)</th><th>Bo (RB/STB)</th><th>μo (cp)</th><th>co (psi⁻¹)</th><th>Z-factor</th><th>Bg (RB/Mscf)</th><th>μg (cp)</th></tr></thead><tbody>{rows}</tbody></table>"
            st.markdown(table_html, unsafe_allow_html=True)

        with tab2:
            pressures = df["P (psia)"].tolist()
            tc1, tc2 = st.columns(2, gap="small")
            with tc1:
                with st.container(border=True):
                    st.markdown('<div class="card-header">SOLUTION GOR (Rs) vs PRESSURE</div>', unsafe_allow_html=True)
                    render_area_chart(pressures, df["Rs (scf/STB)"].tolist(), THEME['accent'], '')
                with st.container(border=True):
                    st.markdown('<div class="card-header">OIL VISCOSITY (μo) vs PRESSURE</div>', unsafe_allow_html=True)
                    render_area_chart(pressures, df["muo (cp)"].tolist(), THEME['accent3'], '')
                with st.container(border=True):
                    st.markdown('<div class="card-header">Z-FACTOR vs PRESSURE</div>', unsafe_allow_html=True)
                    render_area_chart(pressures, df["Z-factor"].tolist(), '#f97316', '')
            with tc2:
                with st.container(border=True):
                    st.markdown('<div class="card-header">OIL FVF (Bo) vs PRESSURE</div>', unsafe_allow_html=True)
                    render_area_chart(pressures, df["Bo (RB/STB)"].tolist(), THEME['accent4'], '')
                with st.container(border=True):
                    st.markdown('<div class="card-header">GAS FVF (Bg) vs PRESSURE</div>', unsafe_allow_html=True)
                    render_area_chart(pressures, df["Bg (RB/Mscf)"].tolist(), THEME['accent2'], '')
                with st.container(border=True):
                    st.markdown('<div class="card-header">GAS VISCOSITY (μg) vs PRESSURE</div>', unsafe_allow_html=True)
                    render_area_chart(pressures, df["mug (cp)"].tolist(), THEME['accent5'], '')

        with tab3:
            Rs_min = f"{df['Rs (scf/STB)'].iloc[-1]:.1f}"
            Bo_min = f"{df['Bo (RB/STB)'].iloc[-1]:.4f}"
            muo_max = f"{df['muo (cp)'].max():.4f}"
            Bg_max = f"{df['Bg (RB/Mscf)'].iloc[-1]:.5f}"
            
            drive = "Solution gas drive is the dominant production mechanism. As reservoir pressure drops below Pb, dissolved gas expands and drives oil to the wellbore. Expect increasing GOR over time." if inputs['gor'] < 3300 else "Gas expansion drive is dominant. The system behaves as a gas or gas-condensate reservoir. Monitor condensate drop-out carefully near dew point."
            gravity = "Gravity drainage may also contribute due to the light oil (API > 35°). " if inputs['api'] > 35 else "Water influx from a connected aquifer could supplement drive energy if present. "

            interp_html = f"<div style='display: flex; flex-direction: column; gap: 12px; padding: 1rem 0;'><div style='display: flex; gap: 12px;'><div style='width:8px; height:8px; border-radius:50%; margin-top:6px; flex-shrink:0; background:{THEME['accent']};'></div><div style='font-size:13px; color:{THEME['muted']};'><strong style='color:{THEME['text']}'>Solution GOR (Rs)</strong> declines from <strong style='color:{THEME['text']}'>{inputs['rs_pb']:.0f}</strong> → <strong style='color:{THEME['text']}'>{Rs_min}</strong> scf/STB as pressure falls below bubble point. Dissolved gas evolves out of solution, reducing the gas available to drive production.</div></div><div style='display: flex; gap: 12px;'><div style='width:8px; height:8px; border-radius:50%; margin-top:6px; flex-shrink:0; background:{THEME['accent4']};'></div><div style='font-size:13px; color:{THEME['muted']};'><strong style='color:{THEME['text']}'>Oil FVF (Bo)</strong> decreases from <strong style='color:{THEME['text']}'>{bo_pb:.4f}</strong> → <strong style='color:{THEME['text']}'>{Bo_min}</strong> RB/STB. Shrinkage occurs as gas liberation reduces the volume of live oil in the reservoir relative to stock-tank conditions.</div></div><div style='display: flex; gap: 12px;'><div style='width:8px; height:8px; border-radius:50%; margin-top:6px; flex-shrink:0; background:{THEME['accent3']};'></div><div style='font-size:13px; color:{THEME['muted']};'><strong style='color:{THEME['text']}'>Oil viscosity (μo)</strong> increases to <strong style='color:{THEME['text']}'>{muo_max}</strong> cp at the lowest pressure step. As lighter components flash off, the remaining oil becomes heavier and harder to produce — expect declining productivity index.</div></div><div style='display: flex; gap: 12px;'><div style='width:8px; height:8px; border-radius:50%; margin-top:6px; flex-shrink:0; background:{THEME['accent2']};'></div><div style='font-size:13px; color:{THEME['muted']};'><strong style='color:{THEME['text']}'>Gas FVF (Bg)</strong> rises to <strong style='color:{THEME['text']}'>{Bg_max}</strong> RB/Mscf at low pressure. Liberated free gas expands significantly. Managing the gas-oil ratio (GOR) at surface becomes critical during late-stage depletion.</div></div><div style='display: flex; gap: 12px;'><div style='width:8px; height:8px; border-radius:50%; margin-top:6px; flex-shrink:0; background:#f97316;'></div><div style='font-size:13px; color:{THEME['muted']};'><strong style='color:{THEME['text']}'>Z-factor</strong> quantifies deviation from ideal gas behavior. Values below 1.0 reflect intermolecular attraction; values above 1.0 indicate repulsion at higher compression states. Use with Bg for accurate gas reserve estimation.</div></div><div style='display: flex; gap: 12px;'><div style='width:8px; height:8px; border-radius:50%; margin-top:6px; flex-shrink:0; background:{THEME['accent5']};'></div><div style='font-size:13px; color:{THEME['muted']};'><strong style='color:{THEME['text']}'>Drive mechanism:</strong> {drive} {gravity}</div></div></div>"
            st.markdown(interp_html, unsafe_allow_html=True)

        st.markdown("<hr style='margin: 1.5rem 0 1rem 0; border-color: " + THEME['border'] + ";'>", unsafe_allow_html=True)

        # ACTION BUTTONS
        btn_col1, btn_col2 = st.columns(2, gap="small")
        
        with btn_col1:
            st.download_button("Export CSV", df.to_csv(index=False).encode('utf-8'), "pvt.csv", "text/csv", use_container_width=True)
            
        with btn_col2:
            print_btn_style = f"background-color:{THEME['bg2']}; background-image:linear-gradient(180deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0) 100%); border:1px solid {THEME['border']}; color:{THEME['text']}; letter-spacing:0.3px; padding:0 14px; border-radius:8px; cursor:pointer; width:100%; font-family:'Inter', sans-serif; font-size:13px; height:36px; display:flex; align-items:center; justify-content:center; transition:all 0.2s ease; font-weight: 500; box-shadow:0 1px 2px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);"
            hover_script = f"onmouseover=\"this.style.borderColor='{THEME['border_hover']}'; this.style.color='{THEME['text']}'; this.style.backgroundImage='linear-gradient(180deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.02) 100%)';\" onmouseout=\"this.style.borderColor='{THEME['border']}'; this.style.color='{THEME['text']}'; this.style.backgroundImage='linear-gradient(180deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0) 100%)';\""
            
            html_content = f"""
            <style>body {{ margin: 0; padding: 0; box-sizing: border-box; }}</style>
            <button onclick='window.parent.print()' style="{print_btn_style}" {hover_script}>Print Report</button>
            """
            components.html(html_content, height=40)

def render_empty_state():
    with st.container(border=True):
        st.markdown('<div class="card-header">RESULTS</div>', unsafe_allow_html=True)
        st.markdown(f"""<div style="text-align:center; padding:6rem 2rem; color:{THEME['muted']};"><div style="font-size:48px; opacity:0.3; margin-bottom: 1.5rem;">⬡</div><div style="font-family:'Inter', sans-serif; font-size:13px;">Enter reservoir data on the left to instantly calculate PVT parameters.</div></div>""", unsafe_allow_html=True)