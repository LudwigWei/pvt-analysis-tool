import streamlit as st
from utils.theme import THEME

def render_input_panel():
    with st.container(border=True):
        st.markdown('<div class="card-header">Reservoir Parameters</div>', unsafe_allow_html=True)

        # 1. THE INPUT FIELDS (At the top)
        def custom_label(name, unit):
            return f"<div style='display: flex; justify-content: space-between; align-items: baseline; white-space: nowrap; gap: 8px; width: 100%;'><span style='font-size: 13px; font-weight: 500;'>{name}</span><span style='font-size: 11px; color: {THEME['muted']}; text-transform: uppercase; letter-spacing: 0.05em;'>{unit}</span></div>"

        col1, col2 = st.columns(2, gap="medium")
        with col1:
            st.markdown(custom_label("API Gravity", "°API"), unsafe_allow_html=True)
            api = st.number_input("api", min_value=1.0, max_value=60.0, value=float(st.session_state.inputs['api']), step=0.5, format="%g", label_visibility="collapsed")
            
            st.markdown(custom_label("Temperature", "°F"), unsafe_allow_html=True)
            temp = st.number_input("temp", min_value=50, max_value=350, value=int(st.session_state.inputs['temp']), step=5, label_visibility="collapsed")
            
            st.markdown(custom_label("Sol. GOR at Pb", "scf/STB"), unsafe_allow_html=True)
            rs_pb = st.number_input("rs_pb", min_value=10, max_value=3000, value=int(st.session_state.inputs['rs_pb']), step=10, label_visibility="collapsed")

        with col2:
            st.markdown(custom_label("Gas Gravity", "air=1.0"), unsafe_allow_html=True)
            gg = st.number_input("gg", min_value=0.5, max_value=1.5, value=float(st.session_state.inputs['gg']), step=0.01, label_visibility="collapsed")
            
            st.markdown(custom_label("Bubble Point", "psia"), unsafe_allow_html=True)
            pb = st.number_input("pb", min_value=100, max_value=8000, value=int(st.session_state.inputs['pb']), step=50, label_visibility="collapsed")
            
            st.markdown(custom_label("Producing GOR", "scf/STB"), unsafe_allow_html=True)
            gor = st.number_input("gor", min_value=0, max_value=100000, value=int(st.session_state.inputs['gor']), step=50, label_visibility="collapsed")

        # Package current inputs
        current_inputs = {"api": api, "gg": gg, "temp": temp, "pb": pb, "rs_pb": rs_pb, "gor": gor}

        # 2. THE RUN BUTTON (Middle)
        if st.button("▶ Run Analysis", type="primary", use_container_width=True):
            st.session_state.analysis_run = True
            st.session_state.analysis_loaded = False  # Reset loaded state to trigger animation
            st.session_state.inputs = current_inputs 

        # 3. CSV UPLOAD (Bottom)
        uploaded_file = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")
        if uploaded_file is not None:
            import pandas as pd
            try:
                df = pd.read_csv(uploaded_file)
                # Map columns ignoring case
                cols_upper = {c.upper(): c for c in df.columns}
                
                mapping = {
                    "API": "api",
                    "TEMP": "temp",
                    "RS_PB": "rs_pb",
                    "GG": "gg",
                    "PB": "pb",
                    "GOR": "gor"
                }
                
                updated = False
                for target_upper, session_key in mapping.items():
                    if target_upper in cols_upper:
                        val = df[cols_upper[target_upper]].iloc[0]
                        st.session_state.inputs[session_key] = float(val)
                        updated = True
                
                if updated:
                    st.rerun()
            except Exception as e:
                st.error(f"Error reading CSV: {e}")

        return current_inputs

def render_correlations_panel():
    with st.container(border=True):
        st.markdown('<div class="card-header">Active Models</div>', unsafe_allow_html=True)
        html_str = f"""
        <div style='display: flex; flex-direction: column; gap: 8px;'>
            <div style='display: flex; justify-content: space-between; align-items: center; padding: 8px 12px; background: {THEME['bg']}; border-radius: 6px; border: 1px solid {THEME['border']};'>
                <span style='font-size: 12px; color: {THEME['muted']};'>Rs, Bo, Pb, co</span>
                <span style='font-size: 12px; color: {THEME['text']}; font-weight: 500;'>Standing</span>
            </div>
            <div style='display: flex; justify-content: space-between; align-items: center; padding: 8px 12px; background: {THEME['bg']}; border-radius: 6px; border: 1px solid {THEME['border']};'>
                <span style='font-size: 12px; color: {THEME['muted']};'>Oil Viscosity</span>
                <span style='font-size: 12px; color: {THEME['text']}; font-weight: 500;'>Beggs-Robinson</span>
            </div>
            <div style='display: flex; justify-content: space-between; align-items: center; padding: 8px 12px; background: {THEME['bg']}; border-radius: 6px; border: 1px solid {THEME['border']};'>
                <span style='font-size: 12px; color: {THEME['muted']};'>Gas Viscosity</span>
                <span style='font-size: 12px; color: {THEME['text']}; font-weight: 500;'>Lee-Gonzalez</span>
            </div>
            <div style='display: flex; justify-content: space-between; align-items: center; padding: 8px 12px; background: {THEME['bg']}; border-radius: 6px; border: 1px solid {THEME['border']};'>
                <span style='font-size: 12px; color: {THEME['muted']};'>Z-factor</span>
                <span style='font-size: 12px; color: {THEME['text']}; font-weight: 500;'>Papay</span>
            </div>
        </div>
        <div style="height: 12px;"></div>
        """
        st.markdown(html_str, unsafe_allow_html=True)