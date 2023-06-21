import streamlit as st
import plotly.express as px
from chat_processing import format_chat

# Streamlit app
st.title("WhatsApp Chat Analyzer 📊")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    dataframe_chat = format_chat(uploaded_file)

    # Basic Metrics
    st.subheader('Basic Metrics')

    #columns are time, user, message
    total_messages = len(dataframe_chat)
    st.write(f'Total messages: {total_messages}')

    total_words = dataframe_chat['message'].str.split().str.len().sum()
    st.write(f'Total words: {total_words}')

    total_characters = dataframe_chat['message'].str.len().sum()
    st.write(f'Total characters: {total_characters}')
    
    # Count the number of messages per user
    user_message_counts = dataframe_chat['user'].value_counts()

    # Create a DataFrame for Plotly
    df_plotly = user_message_counts.reset_index()
    df_plotly.columns = ['user', 'count']

    # Create the pie chart
    fig = px.pie(df_plotly, values='count', names='user', title='Messages per user')
    
    # Display the plot in Streamlit using Plotly
    st.plotly_chart(fig)

    # Message length per user (bar chart with streamlit)
    # Message length per user (bar chart with streamlit)
    st.subheader('Average message length per user in words')

    # Create a DataFrame with the number of words per message
    df_message_lengths = dataframe_chat.copy()
    df_message_lengths['message_length'] = df_message_lengths['message'].str.split().str.len()

    # Calculate the average message length per user
    df_message_length_avg = df_message_lengths.groupby('user')['message_length'].mean()

    # Convert the series into a DataFrame for streamlit's st.bar_chart
    df_message_length_avg = df_message_length_avg.reset_index()
    df_message_length_avg = df_message_length_avg.rename(columns={'message_length': 'Average Message Length', 'user': 'User'})

    # Set user as index
    df_message_length_avg = df_message_length_avg.set_index('User')

    # Create the bar chart
    st.bar_chart(df_message_length_avg)

    # Time Distribution
    st.subheader('Time Distribution')

        # Extract hour from 'time' column
    dataframe_chat['hour'] = dataframe_chat['time'].dt.hour

    # Count the number of messages sent in each hour
    hourly_message_counts = dataframe_chat['hour'].value_counts().sort_index()

    # Create a DataFrame for Plotly
    df_hourly = hourly_message_counts.reset_index()
    df_hourly.columns = ['hour', 'count']

    # Create the bar chart
    fig_hourly = px.bar(df_hourly, x='hour', y='count', title='Number of messages per hour')

    # Display the plot in Streamlit using Plotly
    st.plotly_chart(fig_hourly)

    # Day Distribution
    st.subheader('Day Distribution')

    # Extract day from 'time' column
    dataframe_chat['day'] = dataframe_chat['time'].dt.day_name()

    # Count the number of messages sent on each day
    daily_message_counts = dataframe_chat['day'].value_counts()

    # Order the data by days of the week
    order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily_message_counts = daily_message_counts.reindex(order, fill_value=0)

    # Create a DataFrame for Streamlit
    df_daily = daily_message_counts.reset_index()
    df_daily.columns = ['day', 'count']

    # Set 'day' column as the index
    df_daily.set_index('day', inplace=True)

    # create bar chart 
    st.bar_chart(df_daily)

    st.subheader('Day Distribution per User')

    # Group by 'day' and 'user' and count the number of messages
    grouped = dataframe_chat.groupby(['day', 'user']).size().reset_index()

    # Pivot the DataFrame to have users as columns, days as index, and message counts as values
    pivot_df = grouped.pivot(index='day', columns='user', values=0).reindex(order, fill_value=0)

    # Create the line chart
    st.line_chart(pivot_df)

    
        

    