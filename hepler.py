from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()

def fetch_stats(selected_users,df):
    if selected_users != 'All':
        df = df[df['users'] == selected_users]

    num_chats = df.shape[0]
    words = []
    for i in df['messages']:
        words.extend(i.split())

    #
    num_media = df[(df['messages'] == '‎sticker omitted' ) | (df['messages'] == '‎image omitted') | (df['messages'] == '‎audio omitted') | (df['messages'] == '‎video omitted')].shape[0]

    links = []
    for i in df['messages']:
        links.extend(extract.find_urls(i))

    return num_chats,len(words),num_media,len(links)

def most_active_users(df):
    x = df['users'].value_counts().head()
    df = round((df['users'].value_counts()/df['users'].shape[0])*100,2).reset_index().rename(columns={'index':'name','users':'percent'})
    return x,df

def create_wordcloud(selected_users,df):
    if selected_users != 'All':
        df = df[df['users'] == selected_users]

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color="black")
    df_wc = wc.generate(df['messages'].str.cat(sep= " "))
    return  df_wc

def common_words(selected_users,df):
    if selected_users != 'All':
        df = df[df['users'] == selected_users]

    temp = df[df['users'] != "group notifiaction"]
    temp = temp[(temp['messages'] != '‎sticker' ) | (temp['messages'] != '‎image') | (temp['messages'] != '‎audio') | (temp['messages'] != '‎video')  | (temp['messages'] != 'omitted') ]

    words = []
    f = open('stop_hinglish.txt','r')
    stopwords = f.read()
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stopwords:
                words.append(word)

    final_df = pd.DataFrame(Counter(words).most_common(20))
    return final_df

def emoji_show(selected_users,df):
    if selected_users != 'All':
        df = df[df['users'] == selected_users]

    emojis = []

    for msg in df['messages']:
        emojis.extend([c for c in msg if c in emoji.UNICODE_EMOJI['en']])

        emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def show_monthly_timeline(selected_users,df):
    if selected_users != 'All':
        df = df[df['users'] == selected_users]

    timeline = df.groupby(['year','month_num','month']).count()['messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+" - "+str(timeline['year'][i]))
    
    timeline['time'] = time

    return timeline

def show_daily_timeline(selected_users,df):
    if selected_users != 'All':
        df = df[df['users'] == selected_users]

    timeline = df.groupby('only_date').count()['messages'].reset_index()

    
    return timeline

def show_activity(selected_users,df,typ):
    if selected_users != 'All':
            df = df[df['users'] == selected_users]


    if typ =='day':
        return df['day_name'].value_counts()
    else:
        return df['month'].value_counts()

def activity_heatmap(selected_users,df):
    if selected_users != 'All':
            df = df[df['users'] == selected_users]

    pt = df.pivot_table(index='day_name',columns='period',values='messages',aggfunc='count').fillna(0)

    return pt
        

    