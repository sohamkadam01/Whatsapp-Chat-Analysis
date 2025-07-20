import re
import pandas as pd

def preprocess(data):  
    pattern = r'^(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2})(?:\s|\u202f)?([ap]m) - (.+)'
    lines = data.split('\n') 

    parsed_data = []

    for line in lines:
        match = re.match(pattern, line)
        if match:
            date = match.group(1)
            time = match.group(2)
            am_pm = match.group(3)
            message = match.group(4)
            datetime_str = f'{date} {time} {am_pm}'
            parsed_data.append([datetime_str, message])
        else:
            if parsed_data:
                parsed_data[-1][1] += '\n' + line.strip()

    df = pd.DataFrame(parsed_data, columns=['datetime', 'message'])

    # Try both 2-digit and 4-digit year format
    try:
        df['datetime'] = pd.to_datetime(df['datetime'], format='%d/%m/%y %I:%M %p', errors='raise')
    except:
        df['datetime'] = pd.to_datetime(df['datetime'], format='%d/%m/%Y %I:%M %p', errors='coerce')

    df = df.dropna(subset=['datetime'])

    users = []
    messages = []

    for message in df['message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['messages'] = messages
    df.drop(columns=['message'], inplace=True)

    # Extract datetime components
    df['year'] = df['datetime'].dt.year
    df['month'] = df['datetime'].dt.month_name()
    df['month_num'] = df['datetime'].dt.month
    df['day_name'] = df['datetime'].dt.day_name()
    df['date'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    df['minute'] = df['datetime'].dt.minute
    # df['links_num']=df['messages'].dt.link

    print(df.columns)
    return df
