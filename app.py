import hepler
import streamlit as st
from preprocessor import  preprocess
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(
   page_title="Whatsapp Chat Analysis",
   page_icon="🧊",
   layout="wide",
   initial_sidebar_state="expanded",
)

st.sidebar.title('Whatsapp Chat Analyzer')
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    file = uploaded_file.getvalue()
    data = file.decode("utf-8")
    df = preprocess(data)
    # st.table(df)

    users = df['users'].unique().tolist()
    users.sort()
    users.insert(0,'All')

    selected_user = st.sidebar.selectbox('Select User Options :',users)

    if st.sidebar.button("show analysis"):
        num_msg,tolal_words,num_media,num_links = hepler.fetch_stats(selected_user,df)
        st.title("Total Statistics")
        col1,col2,col3,col4 = st.columns(4,gap="large")

        with col1:
            st.header('Total Messages')
            st.title(num_msg)

        with col2:
            st.header('Total Words')
            st.title(tolal_words)

        with col3:
            st.header('Total Media')
            st.title(num_media)

        with col4:
            st.header('Total Links')
            st.title(num_links)

        #monthly_timeline
        st.title('Monthly Timeline')
        timeline_df = hepler.show_monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline_df['time'],timeline_df['messages'],color='green')
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        #daily timeline
        st.title('Daily Timeline')
        timeline_df = hepler.show_daily_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline_df['only_date'],timeline_df['messages'],color='green')
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        #activity map
        st.title('Activity Map')
        
        col1,col2 = st.columns(2,gap="large")

        with col1:
            st.subheader('Most Busy Day')
            fig,ax = plt.subplots()
            day_df = hepler.show_activity(selected_user,df,'day')
            ax.bar(day_df.index,day_df.values)
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        with col2:
            st.subheader('Most Busy Month')
            fig,ax = plt.subplots()
            month_df = hepler.show_activity(selected_user,df,'month')
            ax.bar(month_df.index,month_df.values,color="orange")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)



        #activity hitmap
        st.title('Weekly Activity HitMap')
        pt = hepler.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(pt)
        st.pyplot(fig)
        

        if selected_user == "All":

            st.title('Most Active Users In Group')
            x,new_df = hepler.most_active_users(df)
            fig,ax = plt.subplots()

            col1,col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation="vertical")
                st.pyplot(fig)

            with col2:
                st.table(new_df)

        st.title('WorldCloud')
        df_wc = hepler.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        st.title('Common Words Used')
        common_word_df = hepler.common_words(selected_user,df)
        fig,ax = plt.subplots()
        ax.barh(common_word_df[0],common_word_df[1])
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        #emoji analysis
        st.title('Common Emoji Used')
        emoji_df = hepler.emoji_show(selected_user,df)
        col1,col2 = st.columns(2,gap="large")

        with col1:
            st.table(emoji_df)
        
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)

            


