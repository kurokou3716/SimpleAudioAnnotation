import streamlit as st 
from streamlit_option_menu import option_menu
import utils, os

#
def annotation_mainpage():
    action = option_menu(
        '',
        ['Configs', 'Annotation', 'Results'],
        icons=['braces-asterisk', 'journals', 'clipboard-data'],
        orientation='horizontal',
        default_index=0
    )
    if action == 'Configs':
        action_configs(dev_mode=False)
    elif action == 'Annotation':
        action_annotation()
    elif action == 'Results':
        action_results()
    
def action_configs(dev_mode=False):
    if dev_mode:
        st.session_state['username'] = 'dev'
        config_file = 'configs/config_text.yaml'
        dataset_file = 'datasets/ViSEC/ViSEC_dataset.csv'
        result_file = 'datasets/ViSEC/default_ViSEC_text_results.csv'
        utils.load_all(
            st.session_state,
            config_file, dataset_file, result_file
        )
        st.success("👌 All configs loaded ")
    else:
        username = st.text_input('Yourname')
        if username != '' and username != st.session_state['username']:
            st.session_state['username'] = username
        st.info(f"Username: {st.session_state['username']}")
        temp_ss_name = utils.get_ss_name(st.session_state['username'])
        if os.path.isfile(temp_ss_name):
            st.write('Checkpoint exist !')
            ss_load = st.button(
                'Load checkpoint',
                on_click=utils.load_results_ss,
            )
            if ss_load:
                st.success("Checkpoint loaded <3")
        if st.session_state['username'] and st.session_state['config_ready'] == False:
            config_file = 'configs/config_text.yaml'
            dataset_file = 'datasets/ViSEC/ViSEC_dataset.csv'
            result_file = 'datasets/ViSEC/default_ViSEC_text_results.csv'
            utils.load_all(
                st.session_state,
                config_file, dataset_file, result_file
            )
            st.session_state['config_ready'] = True
        if not st.session_state['username']:
            st.warning("Enter your name please")
        if st.session_state['username']:
            ss_safe = st.button(
                    'Save checkpoint',
                    on_click=utils.save_results_ss,
                )
            if ss_safe:
                st.success("Checkpoint saved <3")

@st.experimental_fragment
def annotation_fragment():
    utils.annotation_container()

@st.experimental_fragment
def detail_table_fragment():
    col_num, col_start = st.columns(2)
    with col_num:
        num_row = st.selectbox(
            'Num of rows',
            [10, 25, 50, 100]
        )
    with col_start:
        start_from = st.number_input(
            'Start from #',
            value=0,
            min_value=0,
            max_value=st.session_state['num_results'],
            step=num_row
        )
    st.table(
        st.session_state['results'][start_from:start_from+num_row],
    )
    num_done = len([x for x in st.session_state['results']['text'] if x != "V( ) ^ A( )"])
    st.write(f"Done : {num_done}/{st.session_state['num_results']}")

@st.experimental_fragment
def statistic_plot_fragment():
    fig, detail_tables = utils.plot_result_pie()
    st.pyplot(fig)
    detail_cols = st.columns(len(detail_tables))
    for i, field in enumerate(detail_tables):
        with detail_cols[i]:
            st.write(field)
            st.table(detail_tables[field])
    st.write(f"Num sentence: {st.session_state['num_results']}")


def action_annotation(): 
    st.info(f"Current User: {st.session_state['username']}")
    if st.session_state['username']:
        with st.popover("Goto "):
            goto_id = st.number_input(
                'Sentence id',
                value=st.session_state['cur_idx'],
                min_value=0,
                max_value=(st.session_state['num_results']-1),
            )
            if goto_id != st.session_state['cur_idx']:
                st.session_state['cur_idx'] = goto_id
        annotation_fragment()
        

def action_results():
    st.info(f"Current User: {st.session_state['username']}")
    if st.session_state['username']:
        # tab = option_menu(
        #     '',
        #     ['Statistic', 'Detail', 'Export'],
        #     icons=['pie-chart', 'journal-richtext', 'download'],
        #     orientation='horizontal',
        #     default_index=1
        # )
        tab = option_menu(
            '',
            ['Detail', 'Export'],
            icons=['journal-richtext', 'download'],
            orientation='horizontal',
            default_index=0
        )
        if tab == 'Statistic': #TODO
            statistic_plot_fragment()
        elif tab == 'Detail':
            detail_table_fragment()

        elif tab == 'Export':
            outfile_name = st.text_input("Save to file ")
            if outfile_name:
                st.download_button(
                    label='Download results',
                    data=utils.convert_df(st.session_state['results']),
                    file_name=outfile_name,
                    mime="text/csv"
                )