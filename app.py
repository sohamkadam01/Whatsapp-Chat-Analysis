# import streamlit as st
# import preprocessor, helper
# import matplotlib.pyplot as plt
# from textblob import TextBlob
# import pandas as pd
# from googletrans import Translator

# st.sidebar.title("WhatsApp Chat Analyzer")

# uploaded_file = st.sidebar.file_uploader("Choose a file", type=['txt'])

# if uploaded_file is not None:
#     bytes_data = uploaded_file.getvalue()
#     data = bytes_data.decode("utf-8")
#     df = preprocessor.preprocess(data)

#     user_list = df['user'].unique().tolist()
#     if 'group_notification' in user_list:
#         user_list.remove('group_notification')
#     user_list.sort()
#     user_list.insert(0, "Overall")

#     selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

#     # 🔍 Search functionality
#     search_query = st.sidebar.text_input("Search messages/links")

#     if search_query:
#         st.subheader(f"Search Results for '{search_query}'")
#         search_df = df[df['messages'].str.contains(search_query, case=False, na=False)]
#         if not search_df.empty:
#             st.dataframe(search_df[['datetime', 'user', 'messages']])
#         else:
#             st.warning("No results found.")

#     if st.sidebar.button("Show Analysis"):

#         num_messages, total_words, total_media, total_links = helper.fetch_stats(selected_user, df)
#         st.title("Top Statistic")
#         col1, col2, col3, col4 = st.columns(4)
#         with col1:
#             st.header("Total Messages")
#             st.title(num_messages)
#         with col2:
#             st.header("Total Words")
#             st.title(total_words)
#         with col3:
#             st.header("Total Media")
#             st.title(total_media)
#         with col4:
#             st.header("Total Links")
#             link_df, link_no = helper.extract_links(df, selected_user)
#             st.title(link_no)

#         with st.expander("📜 Show All Messages in a chat")        
#          if not link_df.empty:
#             st.dataframe(link_df)
#             st.write(f"Total Links Shared: {len(link_df)}")
#          else:
#             st.info("No links were shared in this chat.")

#         st.title("Daily Timeline")
#         dailytimeline = helper.daily_timeline(selected_user, df)
#         fig, ax = plt.subplots()
#         ax.plot(dailytimeline['date'], dailytimeline['messages'], color='orange')
#         plt.xticks(rotation='vertical')
#         st.pyplot(fig)

#         st.title("Monthly Timeline")
#         timeline = helper.monthly_timeline(selected_user, df)
#         fig, ax = plt.subplots()
#         ax.plot(timeline['time'], timeline['messages'], color='red')
#         plt.xticks(rotation='vertical')
#         st.pyplot(fig)

#         st.title("Activity Map")
#         col1, col2 = st.columns(2)
#         with col1:
#             st.header("Most Busy Day")
#             busy_day = helper.week_activity_map(selected_user, df)
#             fig, ax = plt.subplots()
#             ax.bar(busy_day.index, busy_day.values)
#             st.pyplot(fig)
#         with col2:
#             st.header("Most Busy Month")
#             month_activity = helper.month_activity_map(selected_user, df)
#             fig, ax = plt.subplots()
#             ax.bar(month_activity.index, month_activity.values, color='green')
#             plt.xticks(rotation='vertical')
#             st.pyplot(fig)

#         if selected_user == 'Overall':
#             st.title("Most Busy User")
#             x, new_df = helper.most_busy_user(df)
#             fig, ax = plt.subplots()
#             col1, col2 = st.columns(2)
#             with col1:
#                 ax.bar(x.index, x.values)
#                 plt.xticks(rotation='vertical')
#                 st.pyplot(fig)
#             with col2:
#                 st.dataframe(new_df)

#         st.title("WordCloud")
#         df_wc = helper.create_wordcloud(selected_user, df)
#         if df_wc:
#             fig, ax = plt.subplots()
#             plt.imshow(df_wc)
#             st.pyplot(fig)
#         else:
#             st.info("No words to display in wordcloud.")

#         most_common_df = helper.most_common_words(selected_user, df)
#         fig, ax = plt.subplots()
#         ax.bar(most_common_df['word'], most_common_df['count'])
#         plt.xticks(rotation='vertical')
#         st.title("Most Common Words")
#         st.pyplot(fig)

#         emoji_df = helper.emoji_fun(selected_user, df)
#         st.title("Emoji Analysis")
#         col1, col2 = st.columns(2)
#         with col1:
#             st.dataframe(emoji_df)
#         with col2:
#             if not emoji_df.empty and emoji_df.shape[1] >= 2:
#                 fig, ax = plt.subplots(figsize=(3, 3))
#                 plt.rcParams['font.family'] = 'Segoe UI Emoji'
#                 ax.pie(emoji_df.iloc[:, 1].head(), labels=emoji_df.iloc[:, 0].head(), autopct="%0.2f")
#                 st.pyplot(fig)
#             else:
#                 st.write("No emoji data to display.")

#         # Sentiment Analysis
#         from helper import clean_message, translate_to_english
#         sentiment_df = df.copy()
#         if selected_user != 'Overall':
#             sentiment_df = sentiment_df[sentiment_df['user'] == selected_user]

#         sentiment_df['cleaned'] = sentiment_df['messages'].apply(clean_message)
#         sentiment_df = sentiment_df[sentiment_df['cleaned'].str.strip() != '']
#         sentiment_df['translated'] = sentiment_df['cleaned'].apply(translate_to_english)
#         sentiment_df = sentiment_df[sentiment_df['translated'].notna()]
#         def get_sentiment(text):
#             blob = TextBlob(text)
#             polarity = blob.sentiment.polarity
#             if polarity > 0.1:
#                 return 'Positive', polarity
#             elif polarity < -0.1:
#                 return 'Negative', polarity
#             else:
#                 return 'Neutral', polarity

#         sentiment_df[['sentiment', 'polarity']] = sentiment_df['translated'].apply(
#             lambda x: pd.Series(get_sentiment(x)))

#         st.subheader("Sentiment Overview")
#         sentiment_counts = sentiment_df['sentiment'].value_counts()
#         fig, ax = plt.subplots(figsize=(2, 2))
#         colors = {'Positive': 'green', 'Neutral': 'gray', 'Negative': 'red'}
#         ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%0.1f%%',
#                colors=[colors.get(s, 'blue') for s in sentiment_counts.index])
#         st.pyplot(fig)

#         # st.subheader("Top Messages by Sentiment")
#         translated_only_df = sentiment_df[sentiment_df['translated'] != sentiment_df['cleaned']]

#         def get_top_messages(df, sentiment_label):
#             subset = df[df['sentiment'] == sentiment_label]
#             if sentiment_label == 'Positive':
#                 return subset.sort_values(by='polarity', ascending=False).head(10)
#             elif sentiment_label == 'Negative':
#                 return subset.sort_values(by='polarity').head(10)
#             else:
#                 return subset.sort_values(by='polarity', key=lambda x: abs(x)).head(10)

#         col1, col2, col3 = st.columns(3)
#         # with col1:
#         #     st.markdown("### 😊 Positive (Translated)")
#         #     st.dataframe(get_top_messages(translated_only_df, 'Positive')[['cleaned', 'translated', 'polarity']])
#         # with col2:
#         #     st.markdown("### 😐 Neutral (Translated)")
#         #     st.dataframe(get_top_messages(translated_only_df, 'Neutral')[['cleaned', 'translated', 'polarity']])
#         # with col3:
#         #     st.markdown("### 😡 Negative (Translated)")
#         #     st.dataframe(get_top_messages(translated_only_df, 'Negative')[['cleaned', 'translated', 'polarity']])

#         # 👀 Display all messages if user wants
#         with st.expander("📜 Show All Messages in a chat"):
#             chat_view_df = df if selected_user == "Overall" else df[df['user'] == selected_user]
#             st.dataframe(chat_view_df[['datetime', 'user', 'messages']])



#main code
# import streamlit as st
# import preprocessor, helper
# import matplotlib.pyplot as plt
# from textblob import TextBlob
# import pandas as pd
# from googletrans import Translator

# st.sidebar.title("WhatsApp Chat Analyzer")
# st.sidebar.image('https://i.pinimg.com/736x/84/9b/b6/849bb619d4c6d5005f29155d532c2fd2.jpg')

# uploaded_file = st.sidebar.file_uploader("Choose a file", type=['txt'])

# if uploaded_file is not None:
#     bytes_data = uploaded_file.getvalue()
#     data = bytes_data.decode("utf-8")
#     df = preprocessor.preprocess(data)

#     user_list = df['user'].unique().tolist()
#     if 'group_notification' in user_list:
#         user_list.remove('group_notification')
#     user_list.sort()
#     user_list.insert(0, "Overall")

#     selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

#     # 🔍 Search functionality
#     search_query = st.sidebar.text_input("Search messages/links")

#     if search_query:
#         st.subheader(f"Search Results for '{search_query}'")
#         search_df = df[df['messages'].str.contains(search_query, case=False, na=False)]
#         if not search_df.empty:
#             st.dataframe(search_df[['datetime', 'user', 'messages']])
#         else:
#             st.warning("No results found.")

#     if st.sidebar.button("Show Analysis"):

#         num_messages, total_words, total_media, total_links = helper.fetch_stats(selected_user, df)
#         st.title("Top Statistic")
#         col1, col2, col3, col4 = st.columns(4)
#         with col1:
#             st.header("Total Messages")
#             st.title(num_messages)
#         with col2:
#             st.header("Total Words")
#             st.title(total_words)
#         with col3:
#             st.header("Total Media")
#             st.title(total_media)
#         with col4:
#             st.header("Total Links")
#             link_df, link_no = helper.extract_links(df, selected_user)
#             st.title(link_no)

#         with st.expander("🔗 Show All Shared Links"):
#             if not link_df.empty:
#                 st.dataframe(link_df)
#                 st.write(f"Total Links Shared: {len(link_df)}")
#             else:
#                 st.info("No links were shared in this chat.")

#         with st.expander("📜 Show All Messages in a chat"):
#             chat_view_df = df if selected_user == "Overall" else df[df['user'] == selected_user]
#             st.dataframe(chat_view_df[['datetime', 'user', 'messages']])

        
#         # unique_users = df['user'].unique()
#         # st.sidebar.header("Users in Group")
#         # for user in unique_users:
#         #  st.sidebar.write(user)


#         st.title("Daily Timeline")
#         dailytimeline = helper.daily_timeline(selected_user, df)
#         fig, ax = plt.subplots()
#         ax.plot(dailytimeline['date'], dailytimeline['messages'], color='orange')
#         plt.xticks(rotation='vertical')
#         st.pyplot(fig)

#         st.title("Monthly Timeline")
#         timeline = helper.monthly_timeline(selected_user, df)
#         fig, ax = plt.subplots()
#         ax.plot(timeline['time'], timeline['messages'], color='red')
#         plt.xticks(rotation='vertical')
#         st.pyplot(fig)

#         st.title("Activity Map")
#         col1, col2 = st.columns(2)
#         with col1:
#             st.header("Most Busy Day")
#             busy_day = helper.week_activity_map(selected_user, df)
#             fig, ax = plt.subplots()
#             ax.bar(busy_day.index, busy_day.values)
#             st.pyplot(fig)
#         with col2:
#             st.header("Most Busy Month")
#             month_activity = helper.month_activity_map(selected_user, df)
#             fig, ax = plt.subplots()
#             ax.bar(month_activity.index, month_activity.values, color='green')
#             plt.xticks(rotation='vertical')
#             st.pyplot(fig)

#         if selected_user == 'Overall':
#             st.title("Most Busy User")
#             x, new_df = helper.most_busy_user(df)
#             fig, ax = plt.subplots()
#             col1, col2 = st.columns(2)
#             with col1:
#                 ax.bar(x.index, x.values)
#                 plt.xticks(rotation='vertical')
#                 st.pyplot(fig)
#             with col2:
#                 st.dataframe(new_df)

#         st.title("WordCloud")
#         df_wc = helper.create_wordcloud(selected_user, df)
#         if df_wc is not None:
#             fig, ax = plt.subplots()
#             plt.imshow(df_wc)
#             plt.axis("off")
#             st.pyplot(fig)
#         else:
#             st.info("No words to display in wordcloud.")

#         most_common_df = helper.most_common_words(selected_user, df)
#         fig, ax = plt.subplots()
#         ax.bar(most_common_df['word'], most_common_df['count'])
#         plt.xticks(rotation='vertical')
#         st.title("Most Common Words")
#         st.pyplot(fig)

#         # EMOJI ANALYSIS
#         emoji_df = helper.emoji_fun(selected_user, df)
#         st.title("Emoji Analysis")
#         col1, col2 = st.columns(2)
#         with col1:
#             st.dataframe(emoji_df)
#         with col2:
#             if not emoji_df.empty and emoji_df.shape[1] >= 2:
#                 fig, ax = plt.subplots(figsize=(3, 3))
#                 plt.rcParams['font.family'] = 'Segoe UI Emoji'
#                 ax.pie(emoji_df.iloc[:, 1].head(), labels=emoji_df.iloc[:, 0].head(), autopct="%0.2f")
#                 st.pyplot(fig)
#             else:
#                 st.write("No emoji data to display.")

#         # Sentiment Analysis
#         from helper import clean_message, translate_to_english
#         sentiment_df = df.copy()
#         if selected_user != 'Overall':
#             sentiment_df = sentiment_df[sentiment_df['user'] == selected_user]

#         sentiment_df['cleaned'] = sentiment_df['messages'].apply(clean_message)
#         sentiment_df = sentiment_df[sentiment_df['cleaned'].str.strip() != '']
#         sentiment_df['translated'] = sentiment_df['cleaned'].apply(translate_to_english)
#         sentiment_df = sentiment_df[sentiment_df['translated'].notna()]

#         def get_sentiment(text):
#             blob = TextBlob(text)
#             polarity = blob.sentiment.polarity
#             if polarity > 0.1:
#                 return 'Positive', polarity
#             elif polarity < -0.1:
#                 return 'Negative', polarity
#             else:
#                 return 'Neutral', polarity

#         sentiment_df[['sentiment', 'polarity']] = sentiment_df['translated'].apply(
#             lambda x: pd.Series(get_sentiment(x)))

#         st.subheader("Sentiment Overview")
#         sentiment_counts = sentiment_df['sentiment'].value_counts()
#         fig, ax = plt.subplots(figsize=(2, 2))
#         colors = {'Positive': 'green', 'Neutral': 'gray', 'Negative': 'red'}
#         ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%0.1f%%',
#                colors=[colors.get(s, 'blue') for s in sentiment_counts.index])
#         st.pyplot(fig)

#         # Show all messages in the chat

        
# another code
import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
from textblob import TextBlob
import pandas as pd
from googletrans import Translator

st.sidebar.title("WhatsApp Chat Analyzer")
st.sidebar.image('https://i.pinimg.com/736x/84/9b/b6/849bb619d4c6d5005f29155d532c2fd2.jpg')

uploaded_file = st.sidebar.file_uploader("Choose a file", type=['txt'])

if uploaded_file is not None:
    try:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        df = preprocessor.preprocess(data)

        user_list = df['user'].unique().tolist()
        if 'group_notification' in user_list:
            user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0, "Overall")

        selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

        # 🔍 Search functionality
        search_query = st.sidebar.text_input("Search messages/links")

        if search_query:
            st.subheader(f"Search Results for '{search_query}'")
            search_df = df[df['messages'].str.contains(search_query, case=False, na=False)]
            if not search_df.empty:
                st.dataframe(search_df[['datetime', 'user', 'messages']])
            else:
                st.warning("No results found.")

        if st.sidebar.button("Show Analysis"):

            num_messages, total_words, total_media, total_links = helper.fetch_stats(selected_user, df)
            st.title("Top Statistics")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.header("Total Messages")
                st.title(num_messages)
            with col2:
                st.header("Total Words")
                st.title(total_words)
            with col3:
                st.header("Total Media")
                st.title(total_media)
            with col4:
                st.header("Total Links")
                link_df, link_no = helper.extract_links(df, selected_user)
                st.title(link_no)

            with st.expander("🔗 Show All Shared Links"):
                if not link_df.empty:
                    st.dataframe(link_df)
                    st.write(f"Total Links Shared: {len(link_df)}")
                else:
                    st.info("No links were shared in this chat.")

            with st.expander("📜 Show All Messages in a chat"):
                chat_view_df = df if selected_user == "Overall" else df[df['user'] == selected_user]
                st.dataframe(chat_view_df[['datetime', 'user', 'messages']])

            # Daily Timeline
            st.title("Daily Timeline")
            dailytimeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(dailytimeline['date'], dailytimeline['messages'], color='orange', marker='o')
            plt.xticks(rotation='vertical')
            plt.title("Messages per Day")
            plt.xlabel("Date")
            plt.ylabel("Number of Messages")
            st.pyplot(fig)

            # Monthly Timeline
            st.title("Monthly Timeline")
            timeline = helper.monthly_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['messages'], color='red', marker='o')
            plt.xticks(rotation='vertical')
            plt.title("Messages per Month")
            plt.xlabel("Month")
            plt.ylabel("Number of Messages")
            st.pyplot(fig)

            # Activity Map
            st.title("Activity Map")
            col1, col2 = st.columns(2)
            with col1:
                st.header("Most Busy Day")
                busy_day = helper.week_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_day.index, busy_day.values, color='blue')
                plt.title("Messages per Day of the Week")
                plt.xlabel("Day")
                plt.ylabel("Number of Messages")
                st.pyplot(fig)
            with col2:
                st.header("Most Busy Month")
                month_activity = helper.month_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(month_activity.index, month_activity.values, color='green')
                plt.title("Messages per Month")
                plt.xlabel("Month")
                plt.ylabel("Number of Messages")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            if selected_user == 'Overall':
                st.title("Most Busy User")
                x, new_df = helper.most_busy_user(df)
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values, color='purple')
                plt.title("Messages per User")
                plt.xlabel("User ")
                plt.ylabel("Number of Messages")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
                st.dataframe(new_df)

            # WordCloud
            st.title("WordCloud")
            df_wc = helper.create_wordcloud(selected_user, df)
            if df_wc is not None:
                fig, ax = plt.subplots()
                plt.imshow(df_wc)
                plt.axis("off")
                st.pyplot(fig)
            else:
                st.info("No words to display in wordcloud.")

            # Most Common Words
            most_common_df = helper.most_common_words(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(most_common_df['word'], most_common_df['count'], color='cyan')
            plt.xticks(rotation='vertical')
            plt.title("Most Common Words")
            plt.xlabel("Words")
            plt.ylabel("Count")
            st.pyplot(fig)

            # Emoji Analysis
            emoji_df = helper.emoji_fun(selected_user, df)
            st.title("Emoji Analysis")
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(emoji_df)
            with col2:
                if not emoji_df.empty and emoji_df.shape[1] >= 2:
                    fig, ax = plt.subplots(figsize=(3, 3))
                    plt.rcParams['font.family'] = 'Segoe UI Emoji'
                    ax.pie(emoji_df.iloc[:, 1].head(), labels=emoji_df.iloc[:, 0].head(), autopct="%0.2f")
                    plt.title("Emoji Distribution")
                    st.pyplot(fig)
                else:
                    st.write("No emoji data to display.")

            # Sentiment Analysis
            sentiment_df = df.copy()
            if selected_user != 'Overall':
                sentiment_df = sentiment_df[sentiment_df['user'] == selected_user]

            sentiment_df['cleaned'] = sentiment_df['messages'].apply(helper.clean_message)
            sentiment_df = sentiment_df[sentiment_df['cleaned'].str.strip() != '']
            sentiment_df['translated'] = sentiment_df['cleaned'].apply(helper.translate_to_english)
            sentiment_df = sentiment_df[sentiment_df['translated'].notna()]

            def get_sentiment(text):
                blob = TextBlob(text)
                polarity = blob.sentiment.polarity
                if polarity > 0.1:
                    return 'Positive', polarity
                elif polarity < -0.1:
                    return 'Negative', polarity
                else:
                    return 'Neutral', polarity

            sentiment_df[['sentiment', 'polarity']] = sentiment_df['translated'].apply(
                lambda x: pd.Series(get_sentiment(x)))

            st.subheader("Sentiment Overview")
            sentiment_counts = sentiment_df['sentiment'].value_counts()
            fig, ax = plt.subplots(figsize=(2, 2))
            colors = {'Positive': 'green', 'Neutral': 'gray', 'Negative': 'red'}
            ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%0.1f%%',
                   colors=[colors.get(s, 'blue') for s in sentiment_counts.index])
            plt.title("Sentiment Distribution")
            st.pyplot(fig)

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Please upload a WhatsApp chat file to analyze.")
