#%%
from datetime import datetime
from wtti import Post

#%%
def test_add_comment():
    post = Post(
        text="This is a test post",
        url="https://example.com/test",
        author="Test author",
        platform="Test platform",
        likes=10,
        published_time=datetime.now(),
        title="Test title",
        category="Test category",
    )
    comment_text = "This is a test comment"
    author = "Test commenter"
    likes = 5
    published_time = datetime.now()
    comment_uuid = post.add_comment(comment_text=comment_text, author=author, likes=likes, published_time=published_time)

    assert len(post.comments) == 1
    assert post.comments_count == 1
    assert post.comments[0].text == comment_text
    assert post.comments[0].author == author
    assert post.comments[0].likes == likes
    # assert post.comments[0].published_time == published_time
    assert post.comments[0].url == post.url
    assert post.comments[0].platform == post.platform
    assert post.comments[0].post_id == post.uuid
    assert post.comments[0].uuid == comment_uuid
