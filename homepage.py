import streamlit as st
st.set_page_config(page_title='Homepage', layout='wide')

st.markdown(
    """
    <style>
    .title-wrapper {
        background-color: black;
        padding: 8px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .title {
        color: white;
        margin: 0;
        padding: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """<div class="title-wrapper"><h1 class="title">REVERSED DCF</h1></div>""",
    unsafe_allow_html=True
)


st.write("This site provides interactive tools to valuate and analyze stocks through Reverse DCF model. Check the navigation bar for more.")
