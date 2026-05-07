import streamlit as st
import time
from utils.state import init_session_state
from utils.theme import apply_custom_css
from components.header import render_header
from components.inputs import render_input_panel, render_correlations_panel
from components.results import render_results, render_empty_state

def main():
    st.set_page_config(page_title="PVT Analysis Tool", layout="wide", initial_sidebar_state="collapsed")
    
    init_session_state()
    apply_custom_css()
    
   # Splash Screen (Only show on first load)
    if not st.session_state.splash_dismissed:
        splash_html = """
        <style>
        .splash-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 80vh;
        }
        .splash-logo {
            width: 60px;
            height: 60px;
            border: 2px solid #2DD4BF; /* Industrial mint */
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: rotate 2.5s cubic-bezier(0.68, -0.55, 0.265, 1.55) infinite;
        }
        .splash-logo::after {
            content: '';
            width: 30px;
            height: 30px;
            background-color: #2DD4BF;
            animation: pulse 2.5s ease-in-out infinite;
        }
        .splash-title {
            margin-top: 32px;
            color: #2DD4BF;
            font-size: 24px;
            font-weight: 300;
            letter-spacing: 0.3em;
            text-transform: uppercase;
            animation: fadein 2s ease-in;
            font-family: 'Inter', sans-serif;
        }
        .splash-subtitle {
            margin-top: 8px;
            color: #64748B;
            font-size: 11px;
            letter-spacing: 0.2em;
            font-weight: 400;
            text-transform: uppercase;
            animation: fadein 2.5s ease-in;
            font-family: 'Inter', sans-serif;
        }
        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(180deg); }
        }
        @keyframes pulse {
            0%, 100% { transform: scale(0.8); opacity: 0.5; }
            50% { transform: scale(1.2); opacity: 1; }
        }
        @keyframes fadein {
            0% { opacity: 0; transform: translateY(10px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        </style>
        <div class="splash-container">
            <div class="splash-logo"></div>
            <div class="splash-title">PVT Analysis Tool</div>
            <div class="splash-subtitle">System Initialization</div>
        </div>
        """
        st.markdown(splash_html, unsafe_allow_html=True)
        time.sleep(2.5)
        st.session_state.splash_dismissed = True
        st.rerun()

    # Main App Interface
    render_header()

    # Layout: Two columns - Left for inputs, Right for results
    left_col, right_col = st.columns([1.2, 2.8], gap="medium")

    # Left Column: Input Panels
    with left_col:
        current_inputs = render_input_panel()
        render_correlations_panel()

    # Right Column: Results and Charts (conditionally rendered after analysis run)
    with right_col:
        results_placeholder = st.empty()
        
        # Only render the charts if the button was clicked!
        if st.session_state.analysis_run:
            with results_placeholder.container():
                render_results(st.session_state.inputs)
        else:
            with results_placeholder.container():
                render_empty_state()

if __name__ == "__main__":
    main()