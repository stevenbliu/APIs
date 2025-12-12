# Twitter

## Features

    - Users can post media/text
    - User can comment/respond/like to posts
    - Users can follow/unfollow other users

## Entities

    - Users
        - created_at, updated_at, deleted_at
    - Posts (includes Comments / Replies)
        - metadata, parent_post_id (FK: NULL if own post), text
    - Likes
        - metadata, user_id (FK), post_id (FK)
    - Follows
        - metadata, follower_id (FK), follwed_id (FK)
    - Media
        - metadata, post_id (FK), s3_url

    Users:Posts = 1:M
    Users:Likes = 1:M
    Users:Follows = M:M

    Posts:Posts (parent/child)= 1:M
    Posts:Media = 1:M
    Posts:Likes = 1:M
    Posts:Follows = N/A

    Likes:Follows = N/A

## CRUD

    - Posts
        - new_post = Post(user_id, parent_post_id, text)
        - session.add(new_post)
        - if request.image:
            - new_image = Media(new_post.id, status='pending', s3_url=None)
            - session.add(new_image)
            - get presigned_url -> upload
            - update image status and url on complete
    - Likes
        - new_like = Like(user_id, post_id)
        - session.add(new_like)
    - Follows
        - new_follow = Follow(follower_id, followed_id)
        - session.add(new_follow)

## Queries

    - Timeline
        - Get posts from people you follow
            - query = select(Posts).join(Follow, Follow.followd_id == Post.user_id).where((Follow.follower_id == user_id)).order_by(...).where(Follow.id > cursor_id).limit(10)
            - return session.exec(query).all()
        -
