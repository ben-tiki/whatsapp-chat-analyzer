import streamlit as st
import plotly.express as px
import pandas as pd

def display_basic_metrics(df_chat) -> None:
    '''
    Displays basic metrics about the chat log.
    '''
    
    # METRICS TABLE
    # ------------------------
    total_messages = len(df_chat)
    total_words = df_chat['message'].str.split().str.len().sum()
    total_characters = df_chat['message'].str.len().sum()
    longest_message = df_chat['message'].str.len().max()
    average_message_length = df_chat['message'].str.len().mean()
    top_3_emojis = df_chat['emoji'].value_counts().head(3).index.tolist()

    metrics_data = {
        'Total Messages': total_messages,
        'Total Words': total_words,
        'Total Characters': total_characters,
        'Longest Message': longest_message,
        'Average Message Length': round(average_message_length),
        'Top 3 Emojis': top_3_emojis
    }
    
    # Creating a DataFrame to display the data in a more structured format
    metrics_df = pd.DataFrame.from_dict(metrics_data, orient='index', columns=['Count'])
    st.table(metrics_df)

    # METRIC CHARTS
    # ------------------------
    col1, col2 = st.columns(2)

    # USERS CHATS PIE CHART
    # ------------------------
    user_message_counts = df_chat['user'].value_counts().reset_index()
    user_message_counts.columns = ['user', 'count']

    user_message_counts_fig = px.pie(user_message_counts, values='count', names='user', title='Messages per user')

    # Use the first column to display the pie chart
    col1.plotly_chart(user_message_counts_fig, use_container_width=True)

    # BAR CHART CHAT LENGTH
    # ------------------------ 
    df_chat['message_length'] = df_chat['message'].str.len()
    user_message_length = df_chat.groupby('user')['message_length'].sum().reset_index()
    user_message_length.columns = ['user', 'total_chat_length']

    user_message_length_fig = px.bar(user_message_length, x='user', y='total_chat_length', title='Characters written per user')

    # Use the second column to display the bar chart
    col2.plotly_chart(user_message_length_fig, use_container_width=True)
