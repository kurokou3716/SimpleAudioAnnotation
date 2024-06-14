import streamlit as st
import utils
import sidebar

from mode_annotation import annotation_mainpage
from mode_record import record_mainpage
from mode_tutorial import tutorial_mainpage

# sidebar
mode = sidebar.app_sidebar()
if 'username' not in st.session_state:
    st.session_state['username'] = None   
if 'cur_idx' not in st.session_state:
    st.session_state['cur_idx'] = 0 
if 'config_ready' not in st.session_state:
    st.session_state['config_ready'] = False 

# mainpage 
if mode == 'Annotation':
    # if 'cur_idx' not in st.session_state:
    #     st.session_state['cur_idx'] = 0  
    annotation_mainpage() 
elif mode == 'Record':
    record_mainpage()
elif mode == 'Tutorial':
    tutorial_mainpage()