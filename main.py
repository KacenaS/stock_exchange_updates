import requests
from twilio.rest import Client
import os
import datetime

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
API_KEY_ALPHA = "IVF6NJ4JXOIVJLPR"
API_KEY_NEWS = "16fe1956e7884f42a9b4de5a65a54cb3"
account_sid = 'AC96b6fb8f5123a5cea118f257611772d9'
auth_token = 'd64859ba4cbff182edf85c2aefd0d6df'

# Used https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
parameters_alpha = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": API_KEY_ALPHA
}

response_alha = requests.get("https://www.alphavantage.co/query", params=parameters_alpha)

if response_alha.status_code != 200:
    print(f"Error: API call failed with status code {response_alha.status_code}")
    exit()

time_series = response_alha.json().get("Time Series (Daily)")

if not time_series:
    print("Error: 'Time Series (Daily)' data not found in response.")
    print(response_alha.json())
    exit()


sorted_dates = sorted(time_series.keys(), reverse=True)
yesterday = sorted_dates[0]
day_before_yesterday = sorted_dates[1]

yesterday_close = float(time_series[yesterday]["4. close"])
day_before_yesterday_close = float(time_series[day_before_yesterday]["4. close"])

percentage_difference = round(((yesterday_close - day_before_yesterday_close) / day_before_yesterday_close) * 100, 2)


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

parametres_news = {
    "q": COMPANY_NAME,
    "language": "en",
    "apikey": API_KEY_NEWS
}

response_news = requests.get("https://newsapi.org/v2/everything", params=parametres_news)

articles = response_news.json().get("articles")
three_articles = articles[:3]

formates_articles_list = [f"{STOCK}: {'🔺' if percentage_difference > 0 else '🔻'}{percentage_difference} \nHeadline: {article['title']}. \nBrief: {article['description']}." for article in three_articles]

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 

if percentage_difference > 5 or percentage_difference < -5:
    
    client = Client(account_sid, auth_token)
    for article in formates_articles_list:

        message = client.messages.create(
            from_='+12695754101',
            body=formates_articles_list,
            to='+420736435372'
            )

    print(message.status)


