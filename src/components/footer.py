import streamlit as st

def footer_home():
    st.markdown("""
        <div style="margin-top: 3.5rem; margin-bottom: 1.5rem; display: flex; justify-content: center; align-items: center; border-top: 1px solid rgba(23, 35, 79, 0.1); padding-top: 1.25rem;">
            <div style="
                display: flex;
                align-items: center;
                gap: 12px;
                color: #64748B;
                font-family: 'Outfit', sans-serif;
                font-size: 0.85rem;
                letter-spacing: 0.02em;
            ">
                <span style="font-weight: 700; color: #17234F;">SnapShot Class</span>
                <span style="color: #CBD5E1;">•</span>
                <span>AI Biometric Attendance System</span>
                <span style="color: #CBD5E1;">•</span>
                <span>All Rights Reserved</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

def footer_dashboard():
    st.markdown("""
        <div style="margin-top: 3.5rem; margin-bottom: 1.5rem; display: flex; justify-content: center; align-items: center; border-top: 1px solid rgba(23, 35, 79, 0.1); padding-top: 1.25rem;">
            <div style="
                display: flex;
                align-items: center;
                gap: 12px;
                color: #64748B;
                font-family: 'Outfit', sans-serif;
                font-size: 0.85rem;
                letter-spacing: 0.02em;
            ">
                <span style="font-weight: 700; color: #17234F;">SnapShot Class</span>
                <span style="color: #CBD5E1;">•</span>
                <span>Secure Institutional Portal</span>
                <span style="color: #CBD5E1;">•</span>
                <span>v1.0</span>
            </div>
        </div>
    """, unsafe_allow_html=True)