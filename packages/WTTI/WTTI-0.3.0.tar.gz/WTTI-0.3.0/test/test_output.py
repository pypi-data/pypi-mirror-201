#%%
from wtti.output import posts_to_dataframe
from wtti import Post
import pandas as pd

#%%
def test_posts_to_dataframe():
    
    P1 = Post(
    text="文章內容1",
    url="https://www.google.com",
    author="作者1",
    platform="平台1",
    likes=10,
    published_time="2020-01-01 00:00:00",
    title="文章標題1",
    category="OO板",
    )
    P2 = Post(
        text="文章內容2",
        url="https://www.google.com",
        author="作者2",
        platform="平台1",
        likes=5,
        published_time="2020-02-01 00:00:00",
        title="文章標題2",
        category="OO板",
    )
    P1.add_comment("留言內容1", "留言者1", 1, "2020-01-01 00:00:00")
    P1.add_comment("留言內容2", "留言者2", 2, "2020-01-02 00:00:00")
    
    posts_df, comments_df = posts_to_dataframe([P1, P2], merge=False)
    assert isinstance(posts_df, pd.DataFrame)
    assert len(posts_df) == 2
    assert list(posts_df["author"]) == ['作者1', '作者2']
    assert list(posts_df["title"]) == ['文章標題1', '文章標題2']
    assert list(posts_df["category"]) == ['OO板', 'OO板']
    assert list(posts_df["url"]) == ['https://www.google.com', 'https://www.google.com']
    assert list(posts_df["likes"]) == [10, 5]
    assert list(posts_df["published_timestamp"]) == [1577808000, 1580486400]
    
    assert isinstance(comments_df, pd.DataFrame)
    assert len(comments_df) == 2
    assert list(comments_df["author"]) == ['留言者1', '留言者2']
    assert list(comments_df["post_id"]) == [P1.uuid, P1.uuid]
    assert list(comments_df["likes"]) == [1, 2]
    assert list(comments_df["published_timestamp"]) == [1577808000, 1577894400]
    
    posts_df, comments_df = posts_to_dataframe([P1, P2], merge=True)
    assert isinstance(posts_df, pd.DataFrame)
    assert len(posts_df) == 4
    assert list(posts_df["author"]) == ['作者1', '留言者1', '留言者2', '作者2']
    assert list(posts_df["title"]) == ['文章標題1', '文章標題1', '文章標題1', '文章標題2']
    assert list(posts_df["category"]) == ['OO板', 'OO板', 'OO板', 'OO板']
    assert list(posts_df["url"]) == ['https://www.google.com', 'https://www.google.com', 'https://www.google.com', 'https://www.google.com']
    assert list(posts_df["likes"]) == [10, 1, 2, 5]
    assert list(posts_df["published_timestamp"]) == [1577808000, 1577808000, 1577894400, 1580486400]
    assert list(posts_df["content_type"]) == ['post', 'comment', 'comment', 'post']
    assert len(posts_df.iloc[0]["comments_uuid"]) == 2