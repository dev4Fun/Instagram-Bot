import logging
import random

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

import config
from filter import PostFilter
from post_parser import parse_explore
from strategy import RunForeverStrategy
from tracker import post_tracker
from utils import rand_wait_sec

logging.basicConfig(handlers=[logging.StreamHandler()],
                    level=logging.INFO,
                    format='%(asctime)s [%(levelname).4s] %(message)s',
                    datefmt='%a %d %H:%M:%S')

logger = logging.getLogger()


class AutoLikeBot:
    def __init__(self, driver: WebDriver, post_filter=PostFilter(), running_strategy=RunForeverStrategy()):
        self.driver = driver
        self.post_filter = post_filter
        self.running_strategy = running_strategy

    def __enter__(self):
        if not config.SKIP_LOGIN:
            self.log_in()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()
        logger.info(post_tracker.stats)
        return None

    def like_from_explore(self):
        max_id = 0

        while True:
            try:
                posts = self.fetch_posts_from_explore(max_id)
            except TimeoutException:
                continue
            random.shuffle(posts)
            for post in posts:
                if self.post_filter.should_like(post):
                    self.like_post(post)

                    if not self.running_strategy.should_continue_run():
                        return
                else:
                    post_tracker.skipped_post(post)

            max_id += 1

    def log_in(self):
        self.driver.get("https://www.instagram.com/")
        try:
            self.wait_until(ec.presence_of_element_located((By.NAME, 'username')))

            try:
                self.driver.find_element_by_name('username').send_keys(config.USERNAME)
                self.driver.find_element_by_name('password').send_keys(config.PASSWORD)
                self.driver.find_element_by_xpath(
                    '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[4]/button').click()

            except NoSuchElementException as e:
                logger.warning(f"Could not find element. Error: {e}")
                return

        except TimeoutException:
            pass

        try:
            # remember this browser prompt
            self.driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div/div/section/div/button').click()
        except NoSuchElementException:
            pass

        try:
            # turn on notifications prompt
            self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]").click()
            logger.debug("Skipping turn on notifications")
        except NoSuchElementException:
            pass

        self.wait_until(ec.presence_of_element_located((By.CLASS_NAME, 'C3uDN')))

    def fetch_posts_from_explore(self, max_id=0):
        text = self.load_pre_from_url(
            f"https://www.instagram.com/explore/grid/?is_prefetch=false&omit_cover_media=false&module=explore_popular&use_sectional_payload=true&cluster_id=explore_all%3A0&include_fixed_destinations=true&max_id={max_id}")
        return parse_explore(text)

    def load_pre_from_url(self, url):
        self.open_and_switch_to_tab(url)
        try:
            self.wait_until(ec.presence_of_element_located((By.TAG_NAME, 'pre')), timeout=7)
            return self.driver.find_element_by_tag_name('pre').text
        finally:
            self.close_and_open_tab()

    def open_and_switch_to_tab(self, url):
        handles = self.driver.window_handles
        self.driver.execute_script(f"window.open('{url}');")
        # index based
        self.driver.switch_to.window(self.driver.window_handles[len(handles)])

    def close_and_open_tab(self, tab_index=0):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[tab_index])

    def like_post(self, post):

        self.open_and_switch_to_tab(post.post_link)
        try:
            self.wait_until(ec.presence_of_element_located((By.CLASS_NAME, 'fr66n')))
            self.driver.find_element_by_class_name('fr66n').click()
            post_tracker.liked_post(post)
            logger.info(f"Liked {post}")
            rand_wait_sec()
            return True

        # post might get removed
        except (NoSuchElementException, TimeoutException):
            return False
        finally:
            self.close_and_open_tab()

    def wait_until(self, condition, timeout=5):
        WebDriverWait(self.driver, timeout).until(condition)
