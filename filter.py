from datetime import timedelta, datetime
from typing import Collection

from post_parser import IgPost
from tracker import post_tracker


class PostFilter:
    def __init__(self, like_limit=150, like_videos=True, ignore_tags: Collection = frozenset(),
                 max_time_difference=timedelta(days=7)):
        self.like_limit = like_limit
        self.like_videos = like_videos
        self.ignore_if_has_tags = set(ignore_tags) if not isinstance(ignore_tags, set) else ignore_tags
        self.max_time_difference = max_time_difference

    def should_like(self, post: IgPost) -> bool:
        if post in post_tracker.posts:
            return False
        if (post.is_video and not self.like_videos
                or post.like_count > self.like_limit
                or datetime.utcnow() - post.taken_at_datetime_utc > self.max_time_difference
                or not post.caption_tags.isdisjoint(self.ignore_if_has_tags)):
            return False
        return True


class MyCustomFilter(PostFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def should_like(self, post: IgPost):
        if post_tracker.like_by_user_id[post.owner_id] >= 2:
            return False

        # Prefer posts without too many tags
        return super().should_like(post) and len(post.caption) < 160 and len(post.caption_tags) < 7
