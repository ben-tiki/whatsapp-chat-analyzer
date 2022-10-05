from ctypes import FormatError
import pandas as pd
import re
import nltk
import emoji


def format_chat(chat_path) -> str:
    ''' 
    Uses regular expressions to extract the time, user (sender) and message from the WhatsApp chat log. 

    Arguments: 
        - chat: a string containing a WhatsApp chat log

    Returns: 
        - a pandas dataframe containing the structured chat log (with columns: 'time', 'user', 'message')
    '''
    try:
        dataframe_chat = pd.read_csv(
            chat_path, header=None, delimiter='\n', engine='python')
    except:
        FormatError('The chat log is not in the correct format. Please check the README for more information.')
        return None

    dataframe_chat.columns = ['text']

    # everything bewteen the first pair of brackets is the date and time
    dataframe_chat['time'] = dataframe_chat['text'].str.extract('\[(.*?)\]')

    # everything between the dates and the ':' symbol is the name of the sender
    dataframe_chat['user'] = dataframe_chat['text'].str.extract('(?<=\]\s)(.*?)(?=\:)')

    # messages can have multiple lines, so we need to fill the user column with the previous value
    dataframe_chat['user'] = dataframe_chat['user'].fillna(method='ffill')
    dataframe_chat['time'] = dataframe_chat['time'].fillna(method='ffill')

    # get a list of all the users
    senders = dataframe_chat['user'].unique().tolist()

    # join the list of senders with the '|' symbol
    senders = '|'.join(senders)

    # get everything after the name of the sender and '[' (start of the date and time)
    dataframe_chat['message'] = dataframe_chat['text'].apply(lambda x: re.sub(r'(\[.*?\]\s('+senders+')\:\s)', '', x))

    # remove the first row, which is the title of the chat
    dataframe_chat = dataframe_chat.iloc[1:]

    return dataframe_chat


def set_datatypes(dataframe_chat) -> pd.DataFrame:
    ''' 
    Converts the columns 'time' and 'user' to the datetime and category data types, respectively. 
    'Message' is converted to a string.
    
    This is done to save memory and improve performance.

    Arguments: 
        - dataframe_chat: a pandas dataframe containing the structured chat log (with columns: 'time', 'user', 'message')

    Returns: 
        - a pandas dataframe with the correct datatypes
    '''
    # drop the text column
    del dataframe_chat['text']
    dataframe_chat['time'] = pd.to_datetime(dataframe_chat['time'])
    dataframe_chat['user'] = dataframe_chat['user'].astype('category')
    dataframe_chat['message'] = dataframe_chat['message'].astype('string')

    return dataframe_chat

def clean_text(message) -> str:
    '''
    Cleans the text of a message by removing punctuation, stopwords and converting to lowercase.

    Arguments: 
        - message: a string

    Returns: 
        - a cleaned string
    '''
    
    # make text lowercase
    message = message.lower()
    # remove punctuation
    message = re.sub(r'[^\w\s]', '', message)
    # remove numbers
    message = re.sub(r'\d+', '', message)
    # remove links
    message = re.sub(r'http\S+', '', message)
    # remove emojis
    message = re.sub(r'\\u\S+', '', message)
    # remove words with less than 3 characters
    message = re.sub(r'\b\w{1,3}\b', '', message)
    # remove words with more than 15 characters
    message = re.sub(r'\b\w{15,}\b', '', message)
    # tokenize
    tokens = nltk.word_tokenize(message)
    # initialize lemmatizer
    lemmatizer = nltk.stem.WordNetLemmatizer()
    # lemmatize each word
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    return tokens

def get_emoji(message, language) -> str:
    '''
    Extracts the emojis from a message.

    Arguments: 
        - message: a string

    Returns: 
        - a string containing the emojis
    '''
    # get the emojis from the message (in english, or in the language of the chat)
    emojis = [c for c in message if c in emoji.UNICODE_EMOJI[language]]
    # join the emojis into a string
    emojis = ''.join(emojis)
    
    return emojis