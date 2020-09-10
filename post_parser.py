import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Set


@dataclass
class IgPost:
    post_id: str = field(repr=False)
    shortcode: str
    caption: str
    like_count: int
    comment_count: int
    taken_at_datetime_utc: datetime
    owner_id: str = field(repr=False)
    is_video: bool
    caption_tags: Set[str] = field(default_factory=set)

    def __post_init__(self):
        if not self.caption_tags:
            self.caption_tags = self._parse_caption_tags()

    def __hash__(self):
        return hash(self.post_id)

    def _parse_caption_tags(self):
        tags = set()

        if not self.caption:
            return tags

        s_i = None
        for i, char in enumerate(self.caption):
            if char == "#":
                if s_i:
                    tags.add(self.caption[s_i:i])
                s_i = i + 1
            elif not (char.isalpha() or char.isdigit()) and s_i:
                tags.add(self.caption[s_i:i])
                s_i = None

        return tags

    @property
    def post_link(self):
        return f"https://www.instagram.com/p/{self.shortcode}/"


def parse_explore(str_in):
    def pass_media(media):
        media = media['media']
        media_id = media['id']
        shortcode = media['code']
        like_count = media['like_count']
        caption = ""
        if media['caption']:
            caption = media['caption']['text']
        comment_count = len(media['comments']) if 'comments' in media else 0
        taken_at_time = datetime.utcfromtimestamp(int(media['taken_at']))
        is_video = media['media_type'] != 1
        owner_id = media['user']['pk']

        return IgPost(media_id, shortcode, caption, like_count, comment_count, taken_at_time, owner_id, is_video)

    posts = []
    json_tree = json.loads(str_in)
    sectional_items = json_tree['sectional_items']
    for item in sectional_items:
        if 'medias' in item['layout_content']:
            for media_item in item['layout_content']['medias']:
                posts.append(pass_media(media_item))
        if 'fill_items' in item['layout_content']:
            for media_item in item['layout_content']['fill_items']:
                posts.append(pass_media(media_item))
        if 'two_by_two_item' in item['layout_content'] and 'media' in item['layout_content']['two_by_two_item']:
            posts.append(pass_media(item['layout_content']['two_by_two_item']))
    return list(filter(lambda p: (p is not None), posts))
