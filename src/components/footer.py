import streamlit as st

def footer_home():

    st.markdown(f"""
        <div style="margin-top:2rem; display:flex; gap:6px; justify-content:center; align-items:center;" >
            <p>Created with ❤️ by </p>
            <p style="color: #FFA500; font-weight: bold;">ANKESH</p>
        </div>
        
    """,unsafe_allow_html=True)