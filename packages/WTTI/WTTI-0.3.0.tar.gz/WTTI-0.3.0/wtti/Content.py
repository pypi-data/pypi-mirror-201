import pandas as pd
import uuid
from time import time

class Content:
    """
    Content 為一個抽象類別, 用來定義一個內容物的基本屬性
    並提供一個 to_series 方法, 用來轉換成 pandas.Series

    Attributes:
        uuid: 內容物的 uuid
        created_timestamp: 內容物的建立時間
        modified_timestamp: 內容物的最後修改時間
        data: 內容物的資料
    
    Methods:
        to_series: 將內容物轉換成 pandas.Series
        
    """
    
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.created_timestamp = int(time())
        self.modified_timestamp = self.created_timestamp
        self.data = {
            "uuid": self.uuid,
            "created_timestamp": self.created_timestamp,
            "modified_timestamp": self.modified_timestamp,
        }

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        # 檢查是否為內建屬性
        if key in ["uuid", "created_timestamp", "modified_timestamp"]:
            raise KeyError(f"Can not modify {key}")
        
        # 檢查要修改的屬性是無變化
        if key in self.data and self.data[key] == value:
            return
        # 更新 modified_timestamp
        else:
            self.modified_timestamp = int(time())
            self.data["modified_timestamp"] = self.modified_timestamp
            # 更新屬性
            self.data[key] = value

    def to_series(self):
        return pd.Series(self.data)
