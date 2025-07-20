# from urlextract import URLExtract
# from wordcloud import WordCloud
# import pandas as pd
# from collections import Counter
# from textblob import TextBlob

# extractor = URLExtract()
# def fetch_stats(selected_user, df):
#     words = []

#     if selected_user != 'Overall':
#         df=df[df['user']==selected_user]

#     num_messages=df.shape[0]
#     words=[]
#     for message in df['messages']:
#         words.extend(message.split())

#     num_media_message=df['messages'] == '<Media omitted>'
#     # links=[]
#     # for message in df['messages']:
#     #     links.append(extractor.find_urls(message))
    
    
#     # return num_messages,len(words),len(num_media_message),len(links)
#     links = []
#     for message in df['messages']:
#      links.extend(extractor.find_urls(message))  # ✅ Correctly add actual links
 
#      return num_messages, len(words), num_media_message.sum(), len(links)


# def extract_links(df, selected_user='Overall'):
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     links = []
#     for msg in df['messages']:
#         # Clean common formatting that can break URL detection
#         msg_clean = msg.replace("*", "").replace("🔗", "").strip()
#         links.extend(extractor.find_urls(msg_clean))

#     links = sorted(set(links))  # remove duplicates
#     return pd.DataFrame(links, columns=["Links"]),len(links)




# def most_busy_user(df):
#     x = df['user'].value_counts().head()
#     df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})
#     return x, df

# def create_wordcloud(selected_user, df):
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]
    
#     stopwords = pd.read_csv('wordcloud.csv')['Stopword'].tolist()

#     temp = df[df['user'] != 'group_notification']
#     temp = temp[temp['messages'] != '<Media omitted>']

#     words = []
#     for message in temp['messages']:
#         for word in message.lower().split():
#             if word not in stopwords:
#                 words.append(word)

#     if not words:

#         return None  

#     word_df = pd.DataFrame(words, columns=['words']).astype(str)

#     wc = WordCloud(width=450, height=450, min_font_size=10, background_color='white')
#     df_wc = wc.generate(word_df['words'].str.cat(sep=" "))
#     return df_wc


# def most_common_words(selected_user,df):
#     if selected_user != 'Overall':
#      df=df[df['user']==selected_user]
    
#     stopwords = pd.read_csv('stopwords.csv')['Stopword'].tolist()

#     temp = df[df['user']!= 'group_notification']
#     temp=temp[temp['messages']!='<Media omitted>']

#     words=[]

#     for message in temp['messages']:
#         for word in message.lower().split():
#             if word not in stopwords:
#                 words.append(word)

#     word_counts = Counter(words).most_common(10)
#     most_common_df = pd.DataFrame(word_counts, columns=['word', 'count'])
#     return most_common_df

# import emoji
# def emoji_fun (selected_user,df):
#     if selected_user != 'Overall':
#         df= df[df['user']== selected_user]

#     emojis=[]
#     for message in df['messages']:
#         emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

#     emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

#     return emoji_df

# def monthly_timeline(selected_user,df):
#     if selected_user!= 'Overall':
#         df=df[df['user']==selected_user]

#     timeline=df.groupby(['year','month_num','month']).count()['messages'].reset_index()
    
#     time=[]
#     for i in range (timeline.shape[0]):
#         time.append(timeline['month'][i] + "-" +str(timeline['year'][i]))

#     timeline['time']=time
#     return timeline

# def daily_timeline(selected_user,df):
#     if selected_user !='Overall':
#         df=df[df['user']==selected_user]

#     daily_timeline=df.groupby('date').count()['messages'].reset_index()
#     return daily_timeline

# def week_activity_map(selected_user,df):
#     if selected_user !='Overall':
#         df=df[df['user']==selected_user]

#     return df['day_name'].value_counts()

# def month_activity_map(selected_user,df):
#      if selected_user !='Overall':
#         df=df[df['user']==selected_user]

#      return df['month'].value_counts()   



# from googletrans import Translator
# import re
# import emoji
# from textblob import TextBlob

# translator = Translator()

# # Clean message
# def clean_message(text):
#     if not isinstance(text, str):
#         return ""
    
#     text = text.strip()
    
#     if text == "<Media omitted>":
#         return ""
    
#     # Remove links
#     text = re.sub(r'http\S+|www\.\S+', '', text)
    
#     # Remove emojis
#     text = ''.join(c for c in text if c not in emoji.EMOJI_DATA)
    
#     # Remove special characters
#     text = re.sub(r'[^\w\s]', '', text)
    
#     # Extra whitespace
#     text = re.sub(r'\s+', ' ', text).strip()
    
#     if len(text) < 3:
#         return ""
    
#     return text

# # Translate to English
# def translate_to_english(text):
#     try:
#         if not text:
#             return ""
#         translated = translator.translate(text, dest='en')
#         return translated.text
#     except Exception as e:
#         print(f"[Translation error]: {text} => {e}")
#         return text


from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
from textblob import TextBlob
import emoji
import re
from googletrans import Translator
from langdetect import detect
import streamlit as st

extractor = URLExtract()
translator = Translator()

# ---------- TEXT CLEANING & TRANSLATION ----------

def clean_message(text):
    if not isinstance(text, str):
        return ""

    text = text.strip()

    if text.lower() in ["<media omitted>", "image omitted", "video omitted"]:
        return ""

    
    text = re.sub(r'http\S+|www\.\S+', '', text)

    
    text = ''.join(c for c in text if c not in emoji.EMOJI_DATA)

    
    text = re.sub(r'[^\w\s]', '', text)

    text = re.sub(r'\b\d{5,}\b', '', text)  
    text = re.sub(r'\b\d+\b', '', text)     

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    if len(text) < 3 or text.isdigit():
        return ""
    
    if len(text.split()) < 2:  # Remove one-word messages
     return ""


    return text


# @st.cache_data(show_spinner=False)
# def translate_to_english(text, retries=1):
#     if not text:
#         return None  # None so we can easily drop later
    
#     for _ in range(retries):
#         try:
#             if detect(text) != 'en':
#                 return translator.translate(text, dest='en').text
#             return text
#         except Exception as e:
#             print(f"[Translation error]: {text} => {e}")
    
#     return None  # Return None if all retries fail
from googletrans import Translator

translator = Translator()

def translate_to_english(text):
    try:
        result = translator.translate(text, dest='en')
        return result.text
    except Exception:
        # If translation fails (e.g., network error or invalid input), skip it
        return None


# ---------- STATS & PROCESSING ----------

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    words = []
    for message in df['messages']:
        words.extend(message.split())

    num_media_message = df['messages'] == '<Media omitted>'

    links = []
    for message in df['messages']:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), num_media_message.sum(), len(links)

def extract_links(df, selected_user='Overall'):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    links = []
    for msg in df['messages']:
        msg_clean = msg.replace("*", "").replace("🔗", "").strip()
        links.extend(extractor.find_urls(msg_clean))

    links = sorted(set(links))
    return pd.DataFrame(links, columns=["Links"]), len(links)

def most_busy_user(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})
    return x, df

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    stopwords = pd.read_csv('wordcloud.csv')['Stopword'].tolist()
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>']

    words = []
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stopwords:
                words.append(word)

    if not words:
        return None

    word_df = pd.DataFrame(words, columns=['words']).astype(str)
    wc = WordCloud(width=450, height=450, min_font_size=10, background_color='white')
    df_wc = wc.generate(word_df['words'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    stopwords = pd.read_csv('stopwords.csv')['Stopword'].tolist()
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>']

    words = []
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stopwords:
                words.append(word)

    word_counts = Counter(words).most_common(10)
    most_common_df = pd.DataFrame(word_counts, columns=['word', 'count'])
    return most_common_df

def emoji_fun(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()
    time = [f"{timeline['month'][i]}-{timeline['year'][i]}" for i in range(timeline.shape[0])]
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df.groupby('date').count()['messages'].reset_index()

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()
