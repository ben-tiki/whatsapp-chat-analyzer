import streamlit as st

from chat_processing import format_chat

from sections.basic_metrics import display_basic_metrics
from sections.time_distribution import display_time_distribution
from sections.text_analysis import display_text_analysis

def main():

    # Streamlit app
    st.title("WhatsApp Chat Analyzer 📊")

    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        dataframe_chat = format_chat(uploaded_file)

        # SECTION 1: Basic Metrics
        # ------------------------
        st.subheader('Basic Metrics')
        st.markdown('This section provides some basic KPI metrics about the chat log.')
        st.markdown('---')
        display_basic_metrics(dataframe_chat)

        # SECTION 2: Time Distribution
        # ------------------------
        st.subheader('Time Distribution')
        st.markdown('This section provides some insights about the time distribution of the chats.')
        st.markdown('---')
        display_time_distribution(dataframe_chat)

        # SECTION 3: Text Analysis
        # ------------------------
        st.subheader('Text Analysis')
        st.markdown('This section provides some insights about the text in the chats.')
        st.markdown('---')
        display_text_analysis(dataframe_chat)


if __name__ == "__main__":
    main()  