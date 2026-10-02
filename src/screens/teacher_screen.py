import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card

from src.database.db import (
    check_teacher_exists,
    create_teacher,
    teacher_login,
    get_teacher_subjects,
    get_attendance_for_teacher,
    get_teacher_by_phone,
    update_teacher_password
)
from src.utils.sms_service import send_otp
from src.components.dialog_create_subjects import create_subject_dialog
from src.components.dialog_share_subjects import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog
from src.components.dialog_attendance_record import attendance_result_dialog

from src.pipelines.face_pipeline import predict_attendance
from src.database.config import supabase

from datetime import datetime

import numpy as np
import pandas as pd

from src.components.dialog_voice_attendance import voice_attendance_dialog

from src.auth.auth import require_role


def teacher_screen():

    style_background_dashboard()
    style_base_layout()
    # Already logged-in teacher

    if (
        st.session_state.get('is_logged_in')
        and st.session_state.get('user_role') == 'teacher'
        and "teacher_data" in st.session_state
    ):

        teacher_dashboard()
        return
    # Teacher Registration
    if (
        'teacher_login_type' not in st.session_state
        or st.session_state.teacher_login_type == 'login'
    ):
        teacher_screen_login()

    elif st.session_state.teacher_login_type == 'register':
        teacher_screen_register()

    elif st.session_state.teacher_login_type == 'forgot_password':
        forgot_password()


def teacher_dashboard():

    teacher_data = st.session_state.teacher_data

    c1, c2 = st.columns(2,vertical_alignment='center',gap='xxlarge')

    with c1:
        header_dashboard()

    with c2:
        st.subheader(f"""Welcome,{teacher_data["name"]}""")

        if st.button("Logout",type='secondary',key='loginbackbtn',shortcut='control+backspace'):
            st.session_state['is_logged_in'] = False
            st.session_state['user_role'] = None
            st.session_state['login_type'] = None

            if "teacher_data" in st.session_state:
                del st.session_state.teacher_data

            st.rerun()

    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'

    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        type1 = ("primary" if st.session_state.current_teacher_tab == 'take_attendance' else 'tertiary')

        if st.button('Take Attendance',width='stretch',type=type1,icon=':material/ar_on_you:'):

            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()

    with tab2:
        type2 = ("primary" if st.session_state.current_teacher_tab == 'manage_subjects'else 'tertiary')

        if st.button('Manage Subjects',width='stretch',type=type2,icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = 'manage_subjects'

            st.rerun()

    with tab3:

        type3 = ("primary" if st.session_state.current_teacher_tab == 'attendance_records'else 'tertiary')

        if st.button('Attendance Records',width='stretch',type=type3,icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()

    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()

    if st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()

    footer_dashboard()


def teacher_tab_take_attendance():

    teacher_id = st.session_state.teacher_data['teacher_id']
    st.header("Take attendance")

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning("You haven't created any subject yet! Please create one 😊")
        return

    subject_options = {f"{s['name']} - {s['subject_code']}": s['subject_id'] for s in subjects}

    col1, col2 = st.columns([3, 1],vertical_alignment='bottom')

    with col1:
        selected_subject_label = st.selectbox('Select Subject',options=list(subject_options.keys()))

    with col2:
        if st.button("Add Photos",type='primary',icon=':material/photo_prints:',width='stretch'):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    if st.session_state.attendance_images:
        st.header("Added Photos")

        gallery_cols = st.columns(4)

        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(img,width='stretch',caption=f"Photo {idx+1}")

    has_photos = bool(st.session_state.attendance_images)

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Clear all photos",width='stretch',type='tertiary',icon=":material/delete:",disabled=not has_photos):
            st.session_state.attendance_images = []
            st.rerun()

    with c2:
        has_photos = bool(st.session_state.attendance_images)

        if st.button("Run Face Analysis",width='stretch',type='secondary',icon=":material/analytics:",disabled=not has_photos):
            with st.spinner("Deep Scanning Photos..."):
                all_detected_ids = {}

                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert('RGB'))

                    detected, _, _ = predict_attendance(img_np)

                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)

                            all_detected_ids.setdefault(student_id,[]).append(f"Photo {idx+1}")

                enrolled_res = (supabase.table('subject_students').select("*, students(*)").eq('subject_id',selected_subject_id).execute())
                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning("No student enrolled in this course")
                else:
                    results = []
                    attendance_to_log = []

                    current_timestamp = (datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))

                    for node in enrolled_students:
                        student = node["students"]

                        sources = all_detected_ids.get(int(student['student_id']),[])

                        is_present = len(sources) > 0

                        results.append({
                            "Name": student['name'],
                            "ID": student['student_id'],
                            "Source": (
                                ", ".join(sources)
                                if is_present else "-"
                            ),
                            "Status": (
                                "✅ Present"
                                if is_present else "❌ Absent"
                            )

                        })

                        attendance_to_log.append({
                            'student_id':student['student_id'],
                            'subject_id':selected_subject_id,
                            'timestamp':current_timestamp,
                            'is_present':bool(is_present)
                        })
                    attendance_result_dialog(pd.DataFrame(results),attendance_to_log)

    with c3:
        if st.button("Use Voice Attendance",type='primary',width='stretch',icon=":material/mic:"):
            voice_attendance_dialog(selected_subject_id)


def teacher_tab_manage_subjects():

    teacher_id = st.session_state.teacher_data['teacher_id']

    col1, col2 = st.columns(2)

    with col1:
        st.header("manage subjects")

    with col2:
        if st.button('Create New Subject',width='stretch'):
            create_subject_dialog(teacher_id)

    subjects = get_teacher_subjects(teacher_id)

    if subjects:
        for sub in subjects:
            stats = [
                ("👥","Students",sub['total_students']),
                ("🕰️","Classes",sub['total_classes'])
            ]

            def share_btn():
                if st.button(f"Share Code: {sub['name']}",key=f"share_{sub['subject_code']}",icon=":material/share:"):
                    share_subject_dialog(sub['name'],sub['subject_code'])
                st.space()

            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats,
                footer_callback=share_btn
            )

    else:
        st.info("NO SUBJECT FOUND. CREATE ONE ABOVE")


def teacher_tab_attendance_records():

    st.header("Attendance records")

    teacher_id = st.session_state.teacher_data['teacher_id']

    records = get_attendance_for_teacher(teacher_id)

    if not records:
        return

    data = []

    for r in records:
        timestamp = r.get('timestamp')

        data.append({
            "ts_group":
                timestamp.split(".")[0]
                if timestamp
                else None,

            "Time":
                datetime.fromisoformat(timestamp)
                .strftime("%Y-%m-%d %I:%M %p")
                if timestamp
                else "N'A",

            "Subject":
                r["subjects"]["name"],

            "Subject Code":
                r["subjects"]["subject_code"],

            "is_present":
                bool(r.get("is_present", False))

        })
    df = pd.DataFrame(data)

    summary = (
        df.groupby(
            ["ts_group","Time","Subject","Subject Code"]
        ).agg(
            Present_count=("is_present","sum"),
            Total_count=("is_present","count")
        ).reset_index()
    )

    summary["Attendance Stats"] = (
        "✅"+ summary["Present_count"].astype(str)+ "/" + summary["Total_count"].astype(str) + "Students"
    )

    display_df = (
        summary.sort_values(by="ts_group",ascending=False)[
            [
                "Time",
                "Subject",
                "Subject Code",
                "Attendance Stats"
            ]
        ]
    )

    st.dataframe(display_df,width='stretch',hide_index=True)


def login_teacher(username, password):
    if not username or not password:
        return False

    teacher = teacher_login(username, password)

    if teacher:
        st.session_state.user_role = "teacher"
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True

        return True

    return False


def forgot_password():
    st.subheader("Reset Password")

    phone_number = st.text_input(
        "Enter registered phone number",
        placeholder="9876543210"
    )

    if "reset_otp" not in st.session_state:
        st.session_state.reset_otp = None

    if "reset_teacher" not in st.session_state:
        st.session_state.reset_teacher = None

    if "otp_verified" not in st.session_state:
        st.session_state.otp_verified = False

    if not st.session_state.otp_verified:
        if st.button("Send OTP"):

            if not phone_number:
                st.error("Enter phone number.")
                return

            teacher = get_teacher_by_phone(phone_number)

            if not teacher:
                st.error("No teacher found with this phone number.")
                return

            success, otp = send_otp(phone_number)

            if success:
                st.session_state.reset_otp = otp
                st.session_state.reset_teacher = teacher

                st.success("OTP sent successfully!")
            else:
                st.error("Failed to send OTP.")

        if st.session_state.reset_otp:
            entered_otp = st.text_input("Enter OTP",max_chars=6)

            if st.button("Verify OTP"):
                if entered_otp == st.session_state.reset_otp:

                    st.session_state.otp_verified = True
                    st.success("OTP verified!")
                else:
                    st.error("Invalid OTP.")

    else:
        new_password = st.text_input(
            "New Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        if st.button("Update Password"):
            if not new_password or not confirm_password:
                st.error("All fields are required.")
                return

            if new_password != confirm_password:
                st.error("Passwords don't match.")
                return

            teacher_id = st.session_state.reset_teacher["teacher_id"]

            update_teacher_password(teacher_id,new_password)

            st.success("Password updated successfully!")

            st.session_state.reset_otp = None
            st.session_state.reset_teacher = None
            st.session_state.otp_verified = False


def teacher_screen_login():

    c1, c2 = st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()

    with c2:
        if st.button("Go back to Home",type='secondary',key='loginbackbtn',shortcut='control+backspace'):
            st.session_state['login_type'] = None
            st.rerun()

    st.space()

    st.header('Login using password',text_alignment='center')

    st.space()

    teacher_username = st.text_input(
        "Enter username",
        placeholder='Shreya'
    )

    teacher_pass = st.text_input(
        "Enter password",
        type='password',
        placeholder='enter password'
    )

    st.divider()

    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button('Login',icon=':material/passkey:',shortcut='control+enter',width='stretch'):
            if login_teacher(teacher_username,teacher_pass):
                st.toast("Welcome back!",icon="👋🏻")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid Username and Password")

    with btnc2:
        if st.button('Register Instead',type='primary',icon=':material/passkey:',width='stretch'):
            st.session_state.teacher_login_type = 'register'
            st.rerun()

    st.space()
    # Forgot Password
    if st.button("Forgot Password?",width='stretch',type='tertiary',):
        st.session_state.teacher_login_type = 'forgot_password'

        st.rerun()
    footer_dashboard()


def register_teacher(teacher_username,teacher_name,phone_number,teacher_pass,teacher_cnf_pass,invite_code):

    if (
        not teacher_username
        or not teacher_name
        or not phone_number
        or not teacher_pass
        or not teacher_cnf_pass
        or not invite_code
    ):
        return False, "All fields are required!"

    correct_code = st.secrets.get("TEACHER_INVITE_CODE")

    if not correct_code:
        return False, "Teacher invite code is not configured."

    if invite_code != correct_code:
        return False, "Invalid teacher invite code!"

    if check_teacher_exists(teacher_username):
        return False, "Username already taken!"

    if teacher_pass != teacher_cnf_pass:
        return False, "Password doesn't match"

    try:
        create_teacher(
            teacher_username,
            teacher_pass,
            teacher_name,
            phone_number
        )
        return True, "Successfully Created! Login now"

    except Exception as e:
        return False, "Unexpected Error! "

def teacher_screen_register():
    c1, c2 = st.columns(2,vertical_alignment='center',gap='xxlarge')

    with c1:
        header_dashboard()

    with c2:
        if st.button("Go back to Home",type='secondary',key='loginbackbtn',shortcut='control+backspace'):
            st.session_state['login_type'] = None
            st.rerun()
    st.space()

    st.header('Register your teacher profile')
    st.space()

    teacher_username = st.text_input(
        "Enter username",
        placeholder='Shreya'
    )

    teacher_name = st.text_input(
        "Enter name",
        placeholder='Shreya'
    )

    phone_number = st.text_input(
        "Enter phone number",
        placeholder="9876543210"
    )

    teacher_pass = st.text_input(
        "Enter password",
        type='password',
        placeholder='enter password'
    )

    teacher_cnf_pass = st.text_input(
        "Confirm password",
        type='password',
        placeholder='enter confirm password'
    )
    invite_code = st.text_input(
        "Teacher Invite Code",
        type="password",
        placeholder="Enter teacher invite code"
    )

    st.divider()

    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button('Register now',icon=':material/passkey:',shortcut='control+enter',width='stretch'):
            success, message = register_teacher(
                teacher_username,
                teacher_name,
                phone_number,
                teacher_pass,
                teacher_cnf_pass,
                invite_code
            )

            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type = "login"
                st.rerun()

            else:
                st.error(message)

    with btnc2:
        if st.button('Login Instead',type='primary',icon=':material/passkey:',width='stretch'):
            st.session_state.teacher_login_type = 'login'

            st.rerun()

    footer_dashboard()