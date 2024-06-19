import re
from datetime import datetime
import pandas as pd
def preprocessor(data):
    # # here formate is 12 hour so we change into the 24 hour formate.
    # messages = data.split('\n')
    # modified_messages = []
    #
    # for message in messages:
    #     parts = message.split(' - ', 1)
    #     if len(parts) == 2:
    #         time_str, msg_str = parts
    #         # convert string into the time object
    #         time_obj = datetime.strptime(time_str, "%d/%m/%Y, %I:%M %p")
    #
    #         # Convert time part to 24-hour format and remove AM/PM
    #         time_24_hour = time_obj.strftime("%d/%m/%Y, %H:%M")
    #
    #         # combine msg and 24 hour time formate.
    #         full_time_msg = f"{time_24_hour} - {msg_str}"
    #
    #         # Append the modified message to the list
    #         modified_messages.append(full_time_msg)
    #
    #     else:
    #         modified_messages.append(msg_str)
    # # Join all modified messages into a single variable
    # modified_messages.pop(-1)
    # combined_content = '\n'.join(modified_messages)
#TY...........----------------------------------------------------------------------------
    messages = data.split('\n')
    modified_messages = []

    for message in messages:
        parts = message.split(' - ', 1)
        if len(parts) == 2:
            time_str, msg_str = parts
            try:
                # convert string into the time object
                time_obj = datetime.strptime(time_str, "%d/%m/%Y, %I:%M %p")

                # Convert time part to 24-hour format and remove AM/PM
                time_24_hour = time_obj.strftime("%d/%m/%Y, %H:%M")

                # combine msg and 24 hour time format.
                full_time_msg = f"{time_24_hour} - {msg_str}"

                # Append the modified message to the list
                modified_messages.append(full_time_msg)
            except ValueError:
                # Skip messages that don't match the expected format
                modified_messages.append(message)
        else:
            modified_messages.append(message)

    # Join all modified messages into a single variable
    modified_messages.pop(-1)
    combined_content = '\n'.join(modified_messages)
#------------------------------------------------------------------------------
    # now need to split the data into the 2 columns:
    # 1) Date
    # 2) Message...  so first make regular expression for that.
    # pattern = 'd{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    pattern_date = r'\d{2}/\d{2}/\d{4}, \d{2}:\d{2} -'
    pattern_msg = r'(?<=-\s).+'

    messages = re.findall(pattern_msg, combined_content)
    dates = re.findall(pattern_date, combined_content)

    # create dataframe for message and date.
    if len(messages) > len(dates):
        messages = messages[:len(dates)]
    elif len(messages) < len(dates):
        dates = dates[:len(messages)]
    df = pd.DataFrame({'user_message': messages, 'date': dates})
    df['date'] = pd.to_datetime(df['date'], format="%d/%m/%Y, %H:%M -")

    # now need to seperate users and messages
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        # output : ['', 'Darshan SR', 'This message was deleted']
        # entry --> [1:] --> ['Darshan SR', 'This message was deleted']
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    # set values into the columns.
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # fetch year, month,day, hour, minute.
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    # at the later stage during timeanalysis
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()

    period = []
    for i in df['hour']:
        if i == 23:
            period.append(str(i) + "-" + str('00'))
        elif i == 00:
            period.append(str('00') + "-" + str(i + 1))
        else:
            period.append(str(i) + "-" + str(i + 1))
    df['period'] = period
    return df