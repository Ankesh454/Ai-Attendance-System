import streamlit as st


def init_auth():

    if "role" not in st.session_state:
        st.session_state["role"] = None

    if "login_type" not in st.session_state:
        st.session_state["login_type"] = None

    if "student_data" not in st.session_state:
        st.session_state["student_data"] = None

    if "teacher_data" not in st.session_state:
        st.session_state["teacher_data"] = None

def require_role(required_role):

    current_role = st.session_state.get("role")

    if current_role != required_role:

        st.error("You are not authorized to access this portal.")
        st.stop()