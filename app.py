import streamlit as st # pip install streamlit---> streamlit run app.py
import preprocessing,helper
import plotly.express as px
import plotly.io as pio
pio.templates.default = "plotly_dark"
import matplotlib.pyplot as plt
import seaborn as sns


st.sidebar.title("WhatsApp Chat analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    # st.text(data) --> to show the data on streamlit
    df = preprocessing.preprocessor(data)
    # st.dataframe(df)


    user_list = helper.user_list(df)
    selected_user = st.sidebar.selectbox('Select User : ',user_list)

    if st.sidebar.button('Show Analysis'):
        # receive the count of state.
        msg,word,media,link = helper.fetch_state(df,selected_user)
        st.title('Top Statistics : '+ selected_user)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header('Total Messages')
            st.title(msg)
        with col2:
            st.header('Total Words')
            st.title(word)
        with col3:
            st.header('Media Shared')
            st.title(media)
        with col4:
            st.header('Link Shared')
            st.title(link)

        # Monthly time analysis
        st.title('Monthly Timeline')
        timeline = helper.monthly_time_analysis(selected_user,df)
        fig = px.line(timeline, x='time', y='message', color_discrete_sequence=['green'])
        fig.update_xaxes(tickangle=270, showline=True)
        fig.update_yaxes(showline=True)
        fig.update_layout(height = 700,width = 1200)
        st.plotly_chart(fig)

        # Daily time analysis
        st.title('Daily Timeline')
        daily_timeline = helper.daily_time_analysis(selected_user, df)
        fig = px.line(daily_timeline, x='only_date', y='message', color_discrete_sequence=['blue'])
        fig.update_xaxes(tickangle=270, showline=True)
        fig.update_yaxes(showline=True)
        fig.update_layout(height=700, width=1200)
        st.plotly_chart(fig)

        # Activity Map
        st.title('Activity Map')
        busy_day,busy_month = helper.most_busy_day_month(selected_user,df)
        col1,col2 = st.columns(2)
        with col1:
            st.header('Most busy day')
            fig = px.bar(busy_day, x='day_name', y='count', text_auto=True, color='day_name')
            fig.update_xaxes(tickangle=270)
            st.plotly_chart(fig)

        with col2:
            st.header('Most busy month')
            fig = px.bar(busy_month, x='month', y='count', text_auto=True)
            fig.update_xaxes(tickangle=270)
            st.plotly_chart(fig)

        # Weekly Activity Map
        st.title('Weekly Activity Map')
        user_activity = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_activity,annot=True,linewidths=.10,cmap='PRGn')
        st.pyplot(fig)

        # finding the busiest users in the group
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            busy_user,per_df = helper.most_busy_user(df)
            fig, ax = plt.subplots()
            col1, col2= st.columns(2)

            with col1:
                ax = sns.barplot(busy_user, x='user', y='count', color='red')
                plt.xticks(rotation=90)
                st.pyplot(fig)

                # fig = px.bar(busy_user, x=busy_user.index, y=busy_user.values, text_auto=True)
                # # Update bar color
                # fig.update_traces(marker_color='#0DF9FF')
                # fig.update_layout(xaxis=dict(tickangle=270))
                # st.plotly_chart(fig)
            with col2:
                st.dataframe(per_df)

        # Perform wordcloud
        st.title('WordCloud')
        df_wc = helper.wordcloud_image(selected_user,df)
        fig,ax = plt.subplots()
        ax = plt.imshow(df_wc)
        st.pyplot(fig)

        # most common word
        st.title('Most Common Used Words')
        freq_20 = helper.most_common_word(selected_user,df)
        new_df = freq_20.sort_values('count')# just for set proper in bar not important.
        # fig,ax = plt.subplots()
        # ax = sns.barplot(freq_20, x='count', y='word')
        # st.pyplot(fig)
        fig = px.bar(new_df, x='count', y='word',text_auto=True)
        fig.update_layout(height=600,width=1100)
        st.plotly_chart(fig)

        # most common emojies
        st.title('Emoji Analysis')
        emoji_df = helper.emoji_count(selected_user,df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            # pie plot with top 5 emojis
            fig,ax = plt.subplots()
            ax = plt.pie(emoji_df['count'].head(),labels=emoji_df['emoji'].head(),autopct='%0.2f%%',
                         textprops={'fontsize': 7})
            st.pyplot(fig)



