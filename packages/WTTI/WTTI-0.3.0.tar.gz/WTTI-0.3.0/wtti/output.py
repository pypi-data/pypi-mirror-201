from .Post import Post
import pandas as pd

def posts_to_dataframe(posts, merge=False):
    """
    將一個或多個 Post 物件轉換為 pandas DataFrame 格式。

    Args:
        posts (list or Post): 一個 Post 物件或多個 Post 物件的列表。
        merge (bool): 是否將 post 與其 comments 合併為一個 DataFrame。

    Returns:
        tuple: 如果 merge 為 True，回傳一個包含 posts 與 comments 的 DataFrame。
               如果 merge 為 False，回傳一個包含 posts 的 DataFrame 和一個包含 comments 的 DataFrame。
    """
    
    if not isinstance(posts, list):
        posts = [posts]
        
    if merge:
        post_data = []
        for post in posts:
            # 取出 post 的基本屬性，並將留言數量加入 post_data
            post_dict = post.data
            post_dict["content_type"] = "post"
            post_dict["comments_count"] = post.comments_count
            post_dict["comments_uuid"] = post.comments_uuid
            post_data.append(post_dict)
            # 取出 post 的每一個 comment，並將其轉換為一個字典
            for comment in post.comments:
                comment_dict = comment.data
                # 將 comment 所屬的 post 的 uuid 加入 comment_data
                comment_dict["post_uuid"] = post.uuid
                comment_dict["content_type"] = "comment"
                # 補上 post 的基本屬性
                comment_dict["title"] = post.data["title"]
                comment_dict["category"] = post.data["category"]
                post_data.append(comment_dict)
        # 將 post_data 和 comment_data 分別轉換為 DataFrame
        posts_df = pd.DataFrame(post_data)
        comments_df = None
    else:
        post_data = []
        comment_data = []
        for post in posts:
            # 取出 post 的基本屬性，並將留言數量加入 post_data
            post_dict = post.data
            post_dict["comments_count"] = post.comments_count
            post_data.append(post_dict)
            # 取出 post 的每一個 comment，並將其轉換為一個字典
            for comment in post.comments:
                comment_dict = comment.data
                # 將 comment 所屬的 post 的 uuid 加入 comment_data
                comment_data.append(comment_dict)
        # 將 post_data 和 comment_data 分別轉換為 DataFrame
        posts_df = pd.DataFrame(post_data)
        comments_df = pd.DataFrame(comment_data)
    return posts_df, comments_df