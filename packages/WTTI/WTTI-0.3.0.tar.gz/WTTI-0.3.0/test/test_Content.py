#%%
from wtti import Content
import uuid
from time import time
from random import randint
from time import sleep
import pandas as pd

def test_Content():
    # 建立一個 Content 物件
    created_time = int(time())
    content = Content()
    # 檢查 uuid 是否為 uuid.UUID 物件
    assert isinstance(content["uuid"], uuid.UUID)
    # 檢查 timestamp 是否為 int
    assert isinstance(content["created_timestamp"], int)
    assert isinstance(content["modified_timestamp"], int)
    # 檢查 timestamp 是否為當前時間, 以 5 秒為容許誤差
    assert abs(content["created_timestamp"] - created_time) <= 5
    assert abs(content["modified_timestamp"] - created_time) <= 5
    # 檢查是否可以修改屬性，用隨機數模擬
    sleep(2)
    for _ in range(10):
        key = str(uuid.uuid4())
        value = randint(0, 100)
        content[key] = value
        assert content[key] == value
    # 此時 timestamp 應該要更新
    assert content["modified_timestamp"] > created_time 
    # 檢查若要修改內建屬性會拋出錯誤
    try:
        content["uuid"] = "123"
    except KeyError as e:
        assert str(e) == "'Can not modify uuid'" or str(e) == "Can not modify uuid"
    # 檢查若要修改的屬性值無變化，不會更新 timestamp
    content["test"] = 123
    modified_time = content["modified_timestamp"]
    sleep(2)
    content["test"] = 123
    assert content["modified_timestamp"] == modified_time
    # 檢查 to_series() 是否能正常轉換
    series = content.to_series()
    assert isinstance(series, pd.Series)
    assert series["uuid"] == content["uuid"]
    assert series["created_timestamp"] == content["created_timestamp"]
    assert series["modified_timestamp"] == content["modified_timestamp"]
    