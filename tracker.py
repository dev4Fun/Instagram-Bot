from collections import defaultdict


class PostStats:
    def __init__(self):
        self.liked_count = 0
        self.skipped_count = 0


class _PostTracker:
    def __init__(self):
        self.posts = {}
        self.like_by_user_id = defaultdict(int)
        self.liked_count = 0
        self.skipped_count = 0

    def liked_post(self, post):
        self.posts.get(post, PostStats()).liked_count += 1
        self.like_by_user_id[post.owner_id] += 1
        self.liked_count += 1

    def skipped_post(self, post):
        self.posts.get(post, PostStats()).skipped_count += 1
        self.skipped_count += 1

    @property
    def stats(self):
        return f"Liked: {self.liked_count}, skipped: {self.skipped_count}"


post_tracker = _PostTracker()
