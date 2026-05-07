import streamlit as st
from utils.theme import THEME

def render_header():
    st.markdown(f"""
    <div class="fixed-header">
        <div class="header-inner">
            <div class="logo-group">
                <div class="logo-icon">PVT</div>
                <div>
                    <div class="logo-text">PVT Analysis Tool</div>
                    <div class="logo-sub">Reservoir Engineering</div>
                </div>
            </div>
            <div class="header-badge">Standing · Beggs-Robinson · Papay · LGE</div>
        </div>
    </div>
    """, unsafe_allow_html=True)