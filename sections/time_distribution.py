import streamlit as st
import plotly.express as px

def display_time_distribution(df_chat) -> None:
    '''
    Displays time distribution inssiights about the chat log.
    '''
    
    # TIME DISTRIBUTION CHARTS
    # ------------------------
    col1, col2 = st.columns(2)

    # HOUR DISTRIBUTION
    # ------------------------
    hourly_message_counts = df_chat['hour'].value_counts().sort_index()

    hourly_chats_df = hourly_message_counts.reset_index()
    hourly_chats_df.columns = ['hour', 'count']

    fig_hourly = px.bar(hourly_chats_df, x='hour', y='count', title='Histogram of messages per hour')
    col1.plotly_chart(fig_hourly, use_container_width=True)

    # WEEKDAY DISTRIBUTION
    # ------------------------
    daily_message_counts = df_chat['day_name'].value_counts().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

    daily_chats_df = daily_message_counts.reset_index()
    daily_chats_df.columns = ['day', 'count']

    fig_daily = px.bar(daily_chats_df, x='day', y='count', title='Histogram of messages per day')
    col2.plotly_chart(fig_daily, use_container_width=True)
  
    # TIME SERIES ANALYSIS
    # ------------------------
    fig_timeseries = px.line(df_chat, x='time', color='user', title='Time Series Analysis of Messages per User')
    fig_timeseries.update_layout(legend=dict(x=0, y=1))
    st.plotly_chart(fig_timeseries)