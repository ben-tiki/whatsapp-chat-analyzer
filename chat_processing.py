import pandas as pd

def format_chat(chat_file) -> pd.DataFrame:
    '''
    Extracts the time, user (sender) and message from a WhatsApp chat log.

    Args:
        chat_file (io.BytesIO): a BytesIO object containing a WhatsApp chat log

    Returns:
        pd.DataFrame: a dataframe containing the structured chat log (with columns: 'time', 'user', 'message')
    '''

    try:
        chat_text = chat_file.read().decode('utf-8')
        chat_lines = chat_text.split('\n')

        data = {'time': [], 'user': [], 'message': []}
        current_time, current_user = None, None

        for line in chat_lines:
            try:
                time, user_message = line.split('] ', 1)
                user, message = user_message.split(': ', 1)
                current_time, current_user = time.replace("[", "").strip('\u200e'), user
            except ValueError:  
                # Line is a continuation of a message
                message = line

            data['time'].append(current_time)
            data['user'].append(current_user)
            data['message'].append(message)

        dataframe_chat = pd.DataFrame(data)

        # Drop rows where extraction failed
        dataframe_chat.dropna(inplace=True)  

        # Set the correct datatypes for the DataFrame columns
        dataframe_chat['time'] = pd.to_datetime(dataframe_chat['time'], format='%m/%d/%y %H:%M:%S')
        dataframe_chat['user'] = dataframe_chat['user'].astype('category')
        dataframe_chat['message'] = dataframe_chat['message'].astype('string')

        return dataframe_chat
    
    except Exception as e:
        raise ValueError(f"An error occurred while processing the chat log: {str(e)}")