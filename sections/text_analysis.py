import streamlit as st
import plotly.express as px
import pandas as pd
import nltk
import stylecloud
import os
from collections import defaultdict

def display_text_analysis(df_chat) -> None:
    '''
    Displays time distribution inssiights about the chat log.
    '''
    
    # WORD FREQUENCY
    # ------------------------
    col1, col2 = st.columns(2)
    # Create a list of all words said by all users
    all_words = []
    for message in df_chat['message']:
        all_words.extend(message.split())

    # Create a frequency distribution of all words
    fdist = nltk.FreqDist(all_words)

    # Create a DataFrame for Plotly
    df_fdist = pd.DataFrame.from_dict(fdist, orient='index')
    df_fdist.columns = ['Frequency']
    df_fdist.index.name = 'Word'

    # Sort the DataFrame by word frequency
    df_fdist.sort_values(by='Frequency', ascending=False, inplace=True)

    # Create the bar chart
    fig_fdist = px.bar(df_fdist.head(10), x=df_fdist.head(10).index, y='Frequency', title='Top 10 Words in Chat')

    # Display the plot in Streamlit using Plotly
    col1.plotly_chart(fig_fdist, use_container_width=True)

    # UNIQUE WORDS BY USER
    # ------------------------
    unique_words_by_user = defaultdict(set)

    for index, row in df_chat.iterrows():
        user = row['user']
        message = row['message']
        words = set(message.split())
        unique_words_by_user[user].update(words)

    # Create a DataFrame for unique words
    df_unique_words = pd.DataFrame(list(unique_words_by_user.items()), columns=['User', 'Unique_Words'])
    df_unique_words['Unique_Word_Count'] = df_unique_words['Unique_Words'].apply(len)

    # Create a bar chart for unique words by user
    fig_unique_words = px.bar(df_unique_words, x='User', y='Unique_Word_Count', title='Unique Words by User')
    col2.plotly_chart(fig_unique_words, use_container_width=True)

    # WORD CLOUD
    # ------------------------
    st.subheader('Word Cloud')

    stylecloud_colors = ['#003366', '#336699', '#6699CC', '#99CCFF', '#B3D1FF']

    # Create the word cloud
    stylecloud.gen_stylecloud(text=' '.join(all_words), output_name='wordcloud.png', colors=stylecloud_colors,icon_name='fas fa-comment')

    # Open the image

    # Create columns to center the image
    col1, col2, col3 = st.columns([1, 2, 1])
    col2.image('wordcloud.png', use_column_width=True)

    # Delete the word cloud image
    os.remove('wordcloud.png')