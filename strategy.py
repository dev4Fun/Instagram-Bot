import logging
from abc import abstractmethod

from tracker import post_tracker
from utils import rand_wait_min

logger = logging.getLogger()


class BotRunningStrategy:
    @abstractmethod
    def should_continue_run(self):
        pass


class RunForeverStrategy(BotRunningStrategy):
    def should_continue_run(self):
        return True


class LikeLimitStrategy(BotRunningStrategy):
    def __init__(self, limit=200):
        super().__init__()
        self.limit = limit

    def should_continue_run(self):
        return post_tracker.liked_count < self.limit


class RunForeverWithBreaks(LikeLimitStrategy):
    def should_continue_run(self):
        if post_tracker.liked_count > 0 and post_tracker.liked_count % self.limit == 0:
            logger.info(f"Reached {self.limit} likes. Sleeping.. ")
            rand_wait_min(20, 30)
        return True
