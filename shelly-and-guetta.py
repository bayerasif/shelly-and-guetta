import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time
from telegram import Bot, ParseMode
import os


INTERVAL = 180
token = os.environ['TELEGRAM_TOKEN']
bot = Bot(token=token)

def get_programs_df():
    r = requests.get('https://www.kan.org.il/Radio/getMoreItems.aspx?index=0&progId=1479')
    soup = BeautifulSoup(r.text, 'html.parser')
    li_list = soup.select('li > div > a > div')
    title_list = list(map(lambda t: t.get_text(), li_list))
    splitted_data = map(lambda x: x.split('-'), title_list)
    data = map(lambda x: [elm.strip() for elm in x], splitted_data)
    df = pd.DataFrame(data, columns=['title', 'date'])
    df['date'] = pd.to_datetime(df['date'], dayfirst=True)
    return df

def todays_episode_is_up(df, previous_df):
    today = datetime.today().date() - timedelta(3)
    is_up = df['date'].isin([today]).any()
    there_before = previous_df['date'].isin([today]).any()
    return is_up and not there_before

def generate_message(df):
    today = datetime.today().date() - timedelta(3)
    title = df[df['date'].isin([today])].title.iloc[0]
    date = df[df['date'].isin([today])].date.iloc[0].strftime("%d/%m/%Y")
    msg = f'הפרק בשם "{title}" של תאריך {date} עלה וזמין להאזנה'
    return msg

def main():
    previous_df = get_programs_df()
    while True:
        df = get_programs_df()
        if todays_episode_is_up(df, previous_df):
            msg = generate_message(df)
            bot.send_message(chat_id="@shellyandguetta", text=msg, parse_mode=ParseMode.HTML)
        previous_df = df
        time.sleep(INTERVAL)

if __name__ == '__main__':
    main()
