import re
import pandas as pd


def trimm(str):
    return re.sub(r"[\([{})\]]", "", str)

def preprocess(data):
    pattern = '\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}:\d{1,2}\s(?:AM|PM)\]'
    messages = re.split(pattern, data)[1:]

    dates = list(map(trimm, re.findall(pattern, data)))

    df = pd.DataFrame({'User_message': messages, 'date': dates})
    df['date'] = pd.to_datetime(df['date'], format="%d/%m/%y, %I:%M:%S %p")

    users = []
    msg = []
    for i in df['User_message']:
        data = re.split('([\w\W]+?):\s', i)
        if data[1:]:
            users.append(data[1].strip())
            msg.append(data[2].strip())
        else:
            users.append('group_notification')
            msg.append(data[0].strip())

    df['users'] = users
    df['messages'] = msg
    df.drop(columns=['User_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['sec'] = df['date'].dt.second

    period = []
    for hour in df[['day_name','hour']]['hour']:
        if hour == 23:
            period.append(str(hour)+" -  "+str('00'))
        elif hour == 0:
            period.append(str('00')+" -  "+str(hour+1))
        else:
            period.append(str(hour)+" -  "+str(hour+1))

    df['period'] = period

    return  df
