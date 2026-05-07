import streamlit as st
import plotly.graph_objects as go
from utils.theme import THEME

def hex_to_rgba(hex_color, alpha=0.15):
    h = hex_color.lstrip('#')
    return f'rgba({int(h[0:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)},{alpha})'

def render_area_chart(x, y, color, title_label):
    y_min, y_max = min(y), max(y)
    y_pad = (y_max - y_min) * 0.12 if y_max != y_min else abs(y_max) * 0.1 or 0.1
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y, mode='lines+markers',
        line=dict(color=color, width=1.8), marker=dict(size=7.0, color=color),
        fill='tozeroy', fillcolor=hex_to_rgba(color, 0.18),
        hovertemplate='<b>%{x}</b><br>Value: %{y:.4f}<extra></extra>'
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='IBM Plex Mono', size=10, color='#71717A'),
        margin=dict(l=32, r=12, t=14, b=32), height=180,
        title=dict(text=title_label, font=dict(size=9, color='#71717A'), x=0.01, y=0.92),
        xaxis=dict(autorange='reversed', showgrid=True, gridcolor='#2A2A2D', linecolor='#71717A'),
        yaxis=dict(range=[max(0, y_min - y_pad), y_max + y_pad], showgrid=True, gridcolor="#2A2A2D", linecolor='#71717A'),
        showlegend=False, hovermode='closest',
        hoverlabel=dict(bgcolor='#FFFFFF', bordercolor='#D1D5DB', font=dict(color='#000000', size=12)),
        uirevision='constant',       
        transition=dict(duration=500, easing="cubic-in-out")
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}, theme=None)