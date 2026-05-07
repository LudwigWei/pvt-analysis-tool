import streamlit as st

def init_session_state():
    if 'analysis_run' not in st.session_state:
        st.session_state.analysis_run = False
        
    # We store the inputs in session state so a CSV upload can overwrite them
    if 'inputs' not in st.session_state:
        st.session_state.inputs = {
            "api": 35.0,
            "temp": 180,
            "rs_pb": 650,
            "gg": 0.65,
            "pb": 2500,
            "gor": 650
        }