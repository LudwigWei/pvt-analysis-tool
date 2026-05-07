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
    render_header()

    left_col, right_col = st.columns([1.2, 2.8], gap="medium")

    with left_col:
        current_inputs = render_input_panel()
        render_correlations_panel()

    with right_col:
        results_placeholder = st.empty()
        
        # Only render the charts if the button was clicked!
        if st.session_state.analysis_run:
            
            # Check if we need to show the loading animation for a new run
            if not st.session_state.get("analysis_loaded", False):
                results_placeholder.empty() # Clear out anything inherently bound
                
                with results_placeholder.container():
                    # Custom Modern Loader HTML/CSS
                    loader_html = """
                <style>
                .loader-container {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 60vh;
                    width: 100%;
                }
                .neon-ring {
                    width: 50px;
                    height: 50px;
                    border: 3px solid #27272A;
                    border-top-color: #3B82F6;
                    border-radius: 50%;
                    animation: spin 1s linear infinite, glow 2s ease-in-out infinite;
                }
                .loading-text {
                    margin-top: 24px;
                    color: #A1A1AA;
                    font-size: 14px;
                    font-family: 'Inter', sans-serif;
                    font-weight: 500;
                    letter-spacing: 0.05em;
                    animation: pulse 1.5s ease-in-out infinite;
                }
                @keyframes spin { 
                    0% { transform: rotate(0deg); } 
                    100% { transform: rotate(360deg); } 
                }
                @keyframes glow {
                    0%, 100% { box-shadow: 0 0 10px rgba(59, 130, 246, 0.1); }
                    50% { box-shadow: 0 0 20px rgba(59, 130, 246, 0.4); }
                }
                @keyframes pulse {
                    0%, 100% { opacity: 0.6; }
                    50% { opacity: 1; color: #FAFAFA; text-shadow: 0 0 10px rgba(59, 130, 246, 0.3); }
                }
                </style>
                <div class="loader-container">
                    <div class="neon-ring"></div>
                    <div class="loading-text">Running PVT Correlations...</div>
                </div>
                """
                
                    # Render loader in the placeholder
                    st.markdown(loader_html, unsafe_allow_html=True)
                    time.sleep(3)
                
                # Setup session state and immediately rerun to clear the loader and cleanly render results 
                st.session_state.analysis_loaded = True
                st.rerun()
                
            else:
                with results_placeholder.container():
                    render_results(current_inputs)
        else:
            with results_placeholder.container():
                render_empty_state()

if __name__ == "__main__":
    main()