import streamlit as st 
import utils
import os

#
def statistic_user(username):
    temp_name = utils.get_ss_name(username)
    temp_result = utils.pickle.load(open(temp_name,'rb'))['results']
    num_done = len([x for x in temp_result['text'] if x != " "])
    return {
        'username' : username,
        'done' : num_done,
        'total' : len(temp_result)
    }

def record_mainpage():
    all_temps = os.listdir('temp_session')
    all_users = [x.replace('_temp_ss.pickle','') for x in all_temps]
    temp_details = utils.pd.DataFrame([
        statistic_user(x) for x in all_users
    ])
    st.table(
        temp_details
    )