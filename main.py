import requests
from twilio.rest import Client
import os

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
account_sid = 'AC1eccdbe53e16f3d57848a451fca1da54'
auth_token = os.getenv("MY TWILIO AUTH TOKEN")

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = os.getenv("STOCK_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
stock_parameter = {
    "function": "TIME_SERIES_DAILY",
    "outputsize": "compact",
    "datatype": "json",
    "apikey": STOCK_API_KEY,
    "symbol": STOCK_NAME
}

# STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

with requests.get(STOCK_ENDPOINT, params=stock_parameter) as stock:
    stock.raise_for_status()
    all_stock = [value for (key, value) in stock.json()['Time Series (Daily)'].items()]
    all_key = [key for (key, value) in stock.json()['Time Series (Daily)'].items()]
    yesterday = all_stock[0]
    the_day_before_yesterday = all_stock[1]
    yesterday_high = float(yesterday['2. high'])
    yesterday_open = float(yesterday['1. open'])
    yesterday_close = float(yesterday["4. close"])
    the_day_before_yesterday_close = float(the_day_before_yesterday["4. close"])
    different = yesterday_close - the_day_before_yesterday_close
    up_down = None
    different_percentage = round((different / yesterday_close) * 100)
    abs_different_percentage = abs(different_percentage)
    if different_percentage > 0:
        up_down = f"⬆{abs_different_percentage}"
    else:
        up_down = f"⬇{abs_different_percentage}"
    new_parameter = {
        "qInTitle": COMPANY_NAME,
        "apiKey": NEWS_API_KEY
    }
    if different_percentage > 5:
        with requests.get(NEWS_ENDPOINT, params=new_parameter) as news:
            news.raise_for_status()
            data = news.json()
            data_needed = data["articles"][:3]
            formatted_text = [
                f"{STOCK_NAME}: {up_down}%\n{datas['title']}.\n{datas['description']}."
                for datas in data_needed
            ]
            client = Client(account_sid, auth_token)
            for formatted_text in formatted_text:
                message = client.messages \
                    .create(
                        body=f"{formatted_text}",
                        from_='+12549787460',
                        to='+6285767519916'
                    )

# TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries.
#  e.g. [new_value for (key, value) in dictionary.items()]

# TODO 2. - Get the day before yesterday's closing stock price

# TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20.
#  Hint: https://www.w3schools.com/python/ref_func_abs.asp

# TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day
#  before yesterday.

# TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").

# STEP 2: https://newsapi.org/
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

# TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.

# TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint:
#  https://stackoverflow.com/questions/509211/understanding-slice-notation


# STEP 3: Use twilio.com/docs/sms/quickstart/python
# to send a separate message with each article's title and description to your phone number.

# TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.

# TODO 9. - Send each article as a separate message via Twilio.


# Optional TODO: Format the message like this:
"""TESLA: 🔺2% Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TESLA)?. Brief: We at Insider Monkey 
have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F 
filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus 
market crash. or "TESLA: 🔻5% Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TESLA)?. Brief: We at 
Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the 
SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the 
coronavirus market crash. """
