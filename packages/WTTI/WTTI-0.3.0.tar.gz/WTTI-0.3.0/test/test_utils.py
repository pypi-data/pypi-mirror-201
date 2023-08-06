#%%
from wtti.utils import convert_to_timestamp



#%%
def test_convert_to_timestamp():
    # 測試常見的日期時間格式的輸入
    assert convert_to_timestamp("2022-03-27 12:34:56") == 1648355696

    # 測試timestamp格式的輸入
    assert convert_to_timestamp(1648427696) == 1648427696

    # 測試無效格式的輸入
    try:
        convert_to_timestamp("invalid format")
        assert False, "Should raise ValueError for invalid format"
    except ValueError:
        pass
    
