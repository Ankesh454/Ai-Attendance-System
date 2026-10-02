import streamlit as st

from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen
from src.components.dialog_auto_enroll import auto_enroll_dialog


def main():

    st.set_page_config(
        page_title="SnapShot Class - Making Attendance Faster.",
        page_icon="https://imgs.search.brave.com/nn0vWgrqwbB-BFhhb1Uh45KDTNuepnm9N_M8KivT5Gc/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pbWcu/bWFnbmlmaWMuY29t/L2ZyZWUtdmVjdG9y/L3ZlY3Rvci12aW50/YWdlLWNhbWVyYV81/Mzg3Ni0zNjY4MC5q/cGc_c2VtdD1haXNf/aHlicmlkJnc9NzQw/JnE9ODA"
    )

    # -----------------------------------------
    # Initialize session state
    # -----------------------------------------

    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None

    if 'user_role' not in st.session_state:
        st.session_state['user_role'] = None

    if 'is_logged_in' not in st.session_state:
        st.session_state['is_logged_in'] = False

    # -----------------------------------------
    # AUTHENTICATED USER ROUTING
    # -----------------------------------------

    user_role = st.session_state.get('user_role')

    if user_role == 'student':

        student_screen()

    elif user_role == 'teacher':

        teacher_screen()

    # -----------------------------------------
    # LOGIN SCREEN ROUTING
    # -----------------------------------------

    elif st.session_state['login_type'] == 'student':

        student_screen()

    elif st.session_state['login_type'] == 'teacher':

        teacher_screen()

    # -----------------------------------------
    # HOME SCREEN
    # -----------------------------------------

    else:

        home_screen()

    # -----------------------------------------
    # AUTO ENROLL USING JOIN CODE
    # -----------------------------------------

    join_code = st.query_params.get('join-code')

    if join_code:

        # If user is not currently in student login,
        # send them to student login screen.

        if (
            st.session_state.get('user_role') is None
            and st.session_state.get('login_type') != 'student'
        ):

            st.session_state['login_type'] = 'student'
            st.rerun()

        # Only authenticated students can auto-enroll

        if (
            st.session_state.get('is_logged_in')
            and st.session_state.get('user_role') == 'student'
        ):

            auto_enroll_dialog(join_code)


main()