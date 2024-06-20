import streamlit as st 
import pandas as pd

def show_row(row, title):
    with st.expander(title):
        st.audio(f"flacs/{row['name']}")

def show_type(temp_df, type_):
    rows = temp_df.to_dict('records')
    st.title(type_)
    temp_toggle = st.toggle(
        f'Show {type_}',
        key=f'toggle_{type_}'
    )
    if temp_toggle:
        for idx, row in enumerate(rows):
            show_row(row, f"__({idx})__ {row['name']} | {type_} : {row['score']}")


# sidebar 
with st.sidebar:
    st.title("Demo Audio")
    df = pd.read_csv('example.csv')
    show_type(df[df['type']=='valence'], 'Tích cực')
    show_type(df[df['type']=='arousal'], 'Kích động')
    
# main
st.image('smiley.png', width=70)
st.markdown(open('guide.md','r').read())
st.image("arousal_detail.jpg")
st.image("valence_detail.jpg")