# imports 
import streamlit as st 
import yaml
import os 
import pandas as pd
import pickle

# loads 
@st.cache_data
def load_configs(config_file, index=False):
    try:
        if isinstance(config_file, str) and os.path.isfile(config_file):
            configs = yaml.safe_load(open(config_file))
        else:
            configs =  yaml.safe_load(config_file)
        
        delimiter = configs['pd_delimiter']
        temp_labels = configs['labels']
        labels = {
            temp_labels[k]['fieldname'] : {
                'type' : temp_labels[k]['type'],
                'values' : temp_labels[k]['values']
            }
            for k in temp_labels
        }
        if index:
            result2index = {}
            for k in configs['labels']:
                label = configs['labels'][k]
                result2index[label['fieldname']] = {
                    v : int(i)
                    for i,v in enumerate(label['values'])
                }
        else:
            result2index = None

        return delimiter, labels, result2index

    except Exception as e:
        print('Failed to load config file')
        print(e)

@st.cache_data
def load_dataset(dataset_file, delimiter):
    try:
        rows = pd.read_csv(
            dataset_file,
            delimiter=delimiter
        ).to_dict('records')
        dataset = {}
        for row in rows:
            filename = row.pop('filename')
            dataset[filename] = row
        return dataset
    except Exception as e:
        print('Failed to load config file')
        print(e)

@st.cache_data
def load_results(results_file, delimiter):
    try:
        return pd.read_csv(
            results_file,
            delimiter=delimiter
        )
    except Exception as e:
        print('Failed to load config file')
        print(e)

def load_all(
    ss,
    config_file,
    dataset_file,
    results_file
):
    ss['delimiter'], ss['labels'], ss['result2index'] = load_configs(config_file)
    ss['dataset'] = load_dataset(dataset_file, ss['delimiter'])
    ss['results'] = load_results(results_file, ss['delimiter'])
    ss['num_results'] = len(ss['results'])

# export 
@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')

def submit_annotation(idx):
    for label in st.session_state['labels']:
        temp_type = st.session_state['labels'][label]['type']
        st.session_state['results'].loc[idx, label] = st.session_state[f'temp_{temp_type}_{label}']

def previous_func():
    st.session_state['cur_idx'] -= 1
def next_func():
    st.session_state['cur_idx'] += 1

# components
def annotation_radio(
    fieldname,
    valueList,
    value
):
    return st.radio(
        fieldname.capitalize(),
        valueList,
        index=st.session_state['result2index'][fieldname][value],
        key=f'temp_radio_{fieldname}',
        horizontal=True,
    )
def annotation_textbox(
    fieldname,
    value
):
    return st.text_area(
        fieldname.capitalize(),
        value=value,
        key=f'temp_text_area_{fieldname}'
    )

def annotation_container(
):
    

    idx = int(st.session_state['cur_idx'])
    temp_row = st.session_state['results'].loc[idx]
    temp_name = temp_row['filename']
    temp_path = st.session_state['dataset'][temp_name]['filepath']
    st.write(f"Sentence #{idx} : {temp_name}")
    st.audio(temp_path)
    for label in st.session_state['labels']:
        if st.session_state['labels'][label]['type'] == 'radio': 
            annotation_radio(
                label, 
                st.session_state['labels'][label]['values'],
                temp_row[label]
            )
        elif st.session_state['labels'][label]['type'] == 'text_area':
            annotation_textbox(
                label, 
                temp_row[label]
            )
    col_prev, col_submit, col_next = st.columns(3)

    with col_prev:
        previous_btn = st.button(
            '⏮ Previous',
            on_click=previous_func,
        )
    with col_submit:
        submit_btn = st.button(
            "💾 Submit",
            on_click=submit_annotation,
            args=((idx,))
        )
    with col_next:
        next_btn = st.button(
            '⏭ Next',
            on_click=next_func,
        )
    # st.write(st.session_state['cur_idx'])
    if submit_btn:
        st.success('🤗 Submitted')
    if previous_btn or next_btn:
        st.rerun()
    
# plot
from matplotlib import pyplot as plt
import numpy as np

def autopct_func(pct, allvalues):
    absolute_val = int(pct/ 100.*np.sum(allvalues))
    return f'{pct:.2f}%\n{absolute_val}'

def plot_result_pie():
    labels = st.session_state['labels']
    fig, axs = plt.subplots(1, len(labels))
    detail_tables = {}
    for i, label in enumerate(labels):
        temp_series = st.session_state['results'][label].value_counts()
        detail_tables[label] = temp_series
        axs[i].pie(
            temp_series,
            labels=temp_series.index,
            autopct=lambda pct: autopct_func(pct, temp_series),
            textprops={'fontsize':6}
        )
        axs[i].set_title(label)
    # fig.tight_layout()
    return fig, detail_tables

# session proc
import pickle
def get_ss_name(username):
    return f"temp_session/{username}_temp_ss.pickle"

def save_results_ss():
    temp_name = get_ss_name(st.session_state['username'])
    temp = {
        'cur_idx' : st.session_state['cur_idx'],
        'results' : st.session_state['results']
    }
    pickle.dump(temp, open(temp_name,'wb'))

def load_results_ss():
    temp_name = get_ss_name(st.session_state['username'])
    temp = pickle.load(open(temp_name,'rb'))
    st.session_state['cur_idx'] = temp['cur_idx']
    st.session_state['results'] = temp['results']