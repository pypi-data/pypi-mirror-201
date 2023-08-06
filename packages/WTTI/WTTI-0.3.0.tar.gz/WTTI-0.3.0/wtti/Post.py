from .Text import Text
from .Comment import Comment

class Post(Text):
    """
    Post 為文章儲存單位的實體類別, 定義了一個文章的基本屬性
    
    Attributes:
        text_content: 內容的文字內容
        author: 內容的作者
        published_timestamp: 內容的發布時間
        likes: 內容的讚數
        platform: 內容所在的平台
        url: 內容所在的網址
        title: 內容的標題
        category: 內容的分類
        comments: 內容的留言列表，非直接記錄，而是透過 PostComment 類別記錄
        
    Methods:
        to_series: 將內容物轉換成 pandas.Series
        add_comments: 將留言加入內容物的留言列表
    """
    
    def __init__(self, text="", url="", author="", platform="", likes=-1, published_time=None, title="", category=""):
        super().__init__(text=text, url=url, author=author, platform=platform, likes=likes, published_time=published_time)
        self.comments_count = 0 # 留言數量
        self.comments = [] # 留言列表
        self.comments_uuid = [] # 留言的 uuid 列表
        self.data.update({
            "title": title,
            "category": category,
        })
        
    
    def add_comment(self, comment_text="", author="", likes=-1, published_time=None):
        """
        將留言加入內容物的留言列表
        
        Args:
            comment: 要加入的留言
        """
        # 建立一個 Comment 物件
        comment = Comment(
            text=comment_text, author=author, likes=likes, published_time=published_time, 
            url=self.url, platform=self.platform, post_id=self.uuid,
            )
        # 將該物件加入內容物的留言列表
        self.comments.append(comment)
        # 留言數量 + 1
        self.comments_count += 1
        # 將該留言的 uuid 加入內容物的留言 uuid 列表
        self.comments_uuid.append(comment.uuid)
        return comment.uuid
    
