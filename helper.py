import pandas as pd
import emoji
from collections import Counter
from urlextract import URLExtract
from wordcloud import WordCloud
exctracter = URLExtract() # obejct
def user_list(df):
    user_list = sorted(list(df['user'].unique()))
    user_list.remove('group_notification')
    user_list.insert(0,'Overall')
    return user_list


def fetch_state(df,selected_user):

  if selected_user != 'Overall':
    df = df[df['user']==selected_user]

  # 1. Fetch the total no. of messages.
  msg = df.shape[0]

  # 2. Fetch the total no. of word
  word = []
  for w in df['message']:
      word.extend(w.split())

  # 3. Fetch the totsl no. of media shared
  media = df[df['message'] == '<Media omitted>'].shape[0]

  # 4. Fetch the totsl no. of link shared
  link = []
  for l in df['message']:
      link.extend(exctracter.find_urls(l))

  return msg,len(word),media,len(link)

def most_busy_user(df):
    # fetch only dataframe in which group_notification is not a part
    temp_df = df[df['user'] != 'group_notification']
    new_df = temp_df['user'].value_counts().sort_values(ascending=False).reset_index().head(10)

    # participation
    # find the percentage participation of each in chat.
    per_df = round((temp_df['user'].value_counts().sort_values(ascending=False) / temp_df.shape[0]) * 100,
          2).reset_index().rename(columns={'count': 'participation'})
    return new_df,per_df

def wordcloud_image(selected_user,df):
    f = open('stop_hinglish.txt', 'r')
    stop_word = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # remove group_notification
    temp = df[df['message'] != 'group_notification']
    # remove media omitted messages.
    temp = temp[temp['message'] != '<Media omitted>']

    def remove_stop_word(message):
        y = []
        for i in message.lower().split():
            if i not in stop_word:
                y.append(i)
        return " ".join(y)

    # object of WordCloud
    wc = WordCloud(height=500, width=500, min_font_size=10)
    temp['message'] = temp['message'].apply(remove_stop_word)
    df_wc = wc.generate(temp['message'].str.cat(sep=' '))
    return df_wc

def most_common_word(selected_user,df):
    f = open('stop_hinglish.txt','r')

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # remove group_notification
    temp = df[df['message'] != 'group_notification']
    # remove media omitted messages.
    temp = temp[temp['message'] != '<Media omitted>']
    # remove stop_word ( i have file with hinglish stop_word)
    stop_word = f.read()

    word = []
    for i in temp['message']:
        for j in i.lower().split():
            if j not in stop_word:
                word.append(j)
    freq_20_words = pd.DataFrame(Counter(word).most_common(20), columns=['word', 'count'])
    return freq_20_words

def emoji_count(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emojis = []
    for message in df['message']:
        # emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
        emojis.extend([c for c in message if emoji.is_emoji(c)])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))), columns=['emoji', 'count'])
    return emoji_df

def monthly_time_analysis(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # perform groupby
    timeline = df.groupby(['year', 'month_num', 'month'])['message'].count().reset_index()

    # next need to merge year and month in new columns time
    # so message - y_axis and time - x_axis in plot
    time = []
    for i in range(timeline.shape[0]):
      time.append(timeline['month'][i]+'-'+str(timeline['year'][i]))

    # create new columns with name time.
    timeline['time'] = time

    return timeline

def daily_time_analysis(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # perform groupby on only_date
    daily_timeline = df.groupby('only_date')['message'].count().reset_index()
    return daily_timeline

def most_busy_day_month(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # count the values
    busy_day = df['day_name'].value_counts().reset_index()
    busy_month = df['month'].value_counts().reset_index()
    return busy_day,busy_month

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # now create the pivot table.
    user_activity = pd.pivot_table(df, index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_activity

