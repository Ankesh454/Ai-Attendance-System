import streamlit as st

from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen
from src.components.dialog_auto_enroll import auto_enroll_dialog


from src.database.db import get_student_by_id, get_teacher_by_id

def main():

    st.set_page_config(
        page_title="SnapShot Class - Making Attendance Faster.",
        page_icon="https://imgs.search.brave.com/nn0vWgrqwbB-BFhhb1Uh45KDTNuepnm9N_M8KivT5Gc/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pbWcu/bWFnbmlmaWMuY29t/L2ZyZWUtdmVjdG9y/L3ZlY3Rvci12aW50/YWdlLWNhbWVyYV81/Mzg3Ni0zNjY4MC5q/cGc_c2VtdD1haXNf/aHlicmlkJnc9NzQw/JnE9ODA"
    )

    # -----------------------------------------
    # RESTORE OR SYNC SESSION FROM QUERY PARAMS
    # -----------------------------------------

    param_role = st.query_params.get('role')
    param_uid = st.query_params.get('uid')
    param_page = st.query_params.get('page')

    # If URL specifies a logged-in user, restore session
    if param_role == 'student' and param_uid:
        if not st.session_state.get('is_logged_in') or st.session_state.get('user_role') != 'student':
            student = get_student_by_id(param_uid)
            if student:
                st.session_state['is_logged_in'] = True
                st.session_state['user_role'] = 'student'
                st.session_state['student_data'] = student
            else:
                st.query_params.clear()

    elif param_role == 'teacher' and param_uid:
        if not st.session_state.get('is_logged_in') or st.session_state.get('user_role') != 'teacher':
            teacher = get_teacher_by_id(param_uid)
            if teacher:
                st.session_state['is_logged_in'] = True
                st.session_state['user_role'] = 'teacher'
                st.session_state['teacher_data'] = teacher
            else:
                st.query_params.clear()

    # If URL specifies page (e.g. ?page=student or ?page=teacher), or if empty (home)
    if not st.session_state.get('is_logged_in'):
        st.session_state['user_role'] = None
        if param_page in ['student', 'teacher']:
            st.session_state['login_type'] = param_page
        else:
            # If user pressed browser Back to reach root "/" or unknown page
            st.session_state['login_type'] = None

    # -----------------------------------------
    # ROUTING
    # -----------------------------------------

    if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student':
        student_screen()

    elif st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'teacher':
        teacher_screen()

    elif st.session_state.get('login_type') == 'student':
        student_screen()

    elif st.session_state.get('login_type') == 'teacher':
        teacher_screen()

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