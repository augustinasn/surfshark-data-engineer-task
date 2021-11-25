import os
import subprocess

import streamlit as st

from constants import *


def scheduler_ui(state, name):
    with st.form("scheduler-form"):
        option = st.selectbox("Init a new database after:", SCHEDULER_OPTIONS.keys())
        repeat = st.checkbox("Repeat once")

        schedule_btn = st.form_submit_button("Schedule")

        st.write(os.getcwd())
        st.write(os.listdir())
        st.write(os.environ.get("COMPUTERNAME", False))

        if schedule_btn:
            subprocess.Popen(f"python {SCHEDULER_FILEPATH} {SCHEDULER_OPTIONS[option]} {repeat}",
                             shell=False,
                             close_fds=True)
                             
            st.success(f"Successfully set a trigger to init a new DB, {option} from now.")
