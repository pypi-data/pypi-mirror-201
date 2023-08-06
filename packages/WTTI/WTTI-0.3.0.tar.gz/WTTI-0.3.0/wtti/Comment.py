from .Text import Text

class Comment(Text):
    """
    Comment 為留言儲存單位的實體類別, 定義了一個留言的基本屬性
    
    Attributes:
        text_content: 內容的文字內容
        author: 內容的作者
        published_timestamp: 內容的發布時間
        likes: 內容的讚數
        platform: 內容所在的平台
        url: 內容所在的網址
        ---
        post_id: 內容所在的文章的 id
        comments: 留言的留言列表， # TODO: 未來可能會有，目前先保留
        
    Methods:
        to_series: 將內容物轉換成 pandas.Series
        add_comments: 將留言加入內容物的留言列表
    """
    
    def __init__(self, text="", url="", author="", platform="", likes=-1, published_time=None, post_id=None):
        super().__init__(text=text, url=url, author=author, platform=platform, likes=likes, published_time=published_time)
        self.post_id = post_id
        self.data.update({
            "post_id": post_id,
        })
        
    