#%%
from wtti import Text
import uuid
from random import randint
from time import sleep
import pandas as pd
from datetime import datetime
import dateutil
tz = dateutil.tz.gettz('Asia/Taipei')

#%%
def test_text_content():
    text = Text(text="Hello world!")
    assert text.text == "Hello world!"
    text.text = "Hello pytest!"
    assert text.text == "Hello pytest!"

def test_author():
    text = Text(author="John Doe")
    assert text.author == "John Doe"
    text.author = "Jane Smith"
    assert text.author == "Jane Smith"

def test_published_time():
    # 測試輸入 datetime 物件
    time = datetime(2022, 1, 1, 12, 0, 0)
    text = Text(published_time=time)
    assert text.published_time == time.timestamp()
    new_time = datetime(2023, 3, 28, 12, 0, 0)
    text.published_time = new_time.timestamp()
    assert text.published_time == new_time.timestamp()
    # 測試輸入 timestamp
    time = datetime(2022, 1, 1, 12, 0, 0).timestamp()
    text = Text(published_time=time)
    assert text.published_time == time
    # 測試輸入字串
    time = "2023-03-28 12:00:00"
    text = Text(published_time=time)
    assert text.published_time == datetime.strptime(time, "%Y-%m-%d %H:%M:%S").replace(tzinfo=tz).timestamp()

def test_likes():
    text = Text(likes=10)
    assert text.likes == 10
    text.likes = 20
    assert text.likes == 20

def test_platform():
    text = Text(platform="Twitter")
    assert text.platform == "Twitter"
    text.platform = "Facebook"
    assert text.platform == "Facebook"

def test_url():
    text = Text(url="https://example.com")
    assert text.url == "https://example.com"
    
#%%
datetime(2022, 1, 1, 12, 0, 0).timestamp()