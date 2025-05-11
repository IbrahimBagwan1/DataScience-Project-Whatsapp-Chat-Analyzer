import re
import pandas as pd

def preprocess(data):
  f = open("WhatsApp Chat with AIML - 2023 Batch.txt", encoding='utf-8')
  data = f.read()
  pattern = r'\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\u202f[AP]M\s-\s'

  messages = re.split(pattern, data)[1:]

  dates = re.findall(pattern, data)
  dates = [d.replace('\u202f', ' ').replace(' -', '').strip() for d in dates]
  df = pd.DataFrame({'user_message': messages, 'date': dates})

  users = []
  messages = []

  for message in df['user_message']:
      entry = re.split(r'(^[^:]+):\s', message, maxsplit=1)
      if len(entry) > 2:
          users.append(entry[1])
          messages.append(entry[2])
      else:
          users.append('group_notification')
          messages.append(entry[0])

  df['user'] = users
  df['message'] = messages
  df.drop(columns=['user_message'], inplace=True)

  # Convert the date column to datetime
  df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y, %I:%M %p')

  # Extract year, month, etc
  df['only_date'] = df['date'].dt.date
  df['year'] = df['date'].dt.year
  df['month_num'] = df['date'].dt.month
  df['month'] = df['date'].dt.month_name()
  df['day'] = df['date'].dt.day
  df['day_name'] = df['date'].dt.day_name()
  df['hour'] = df['date'].dt.hour
  df['minute'] = df['date'].dt.minute



  period = []
  for hour in df[['day_name', 'hour']]['hour']:
    if hour == 23:
        period.append(str(hour) + "-" + str('00'))
    elif hour == 0:
        period.append(str('00') + "-" + str(hour + 1))
    else:
        period.append(str(hour) + "-" + str(hour + 1))

  df['period'] = period

  return df


