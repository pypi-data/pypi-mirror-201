from datetime import datetime
import dateutil
tz = dateutil.tz.gettz('Asia/Taipei')


def convert_to_timestamp(time_input):
    """
        自動判斷輸入的時間格式，並轉換成timestamp
        支援的時間格式有：
            1. timestamp
            2. "%Y-%m-%d %H:%M:%S"
            3. datetime.datetime
    """
    # datetime格式
    if isinstance(time_input, datetime):
        # 考慮到有可能輸入的datetime沒有設定時區，所以這邊強制設定成台北時區
        time_input = time_input.astimezone(tz)
        return int(time_input.timestamp())
    try:
        # timestamp格式
        timestamp = datetime.fromtimestamp(int(time_input), tz=tz)
    except (ValueError, TypeError):
        try:
            # 常見的日期時間格式
            timestamp = datetime.strptime(time_input, "%Y-%m-%d %H:%M:%S").replace(tzinfo=tz)
            timestamp = timestamp.astimezone(tz)
            
        except (ValueError, TypeError):
            # 如果都不是上述格式，拋出例外
            raise ValueError("Invalid time format, please use timestamp or '%Y-%m-%d %H:%M:%S' format.")
    return int(timestamp.timestamp())
