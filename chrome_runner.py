import pathlib

from selenium import webdriver

import config
from bot import AutoLikeBot
from filter import MyCustomFilter
from strategy import RunForeverWithBreaks


def configure_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={pathlib.Path(__file__).parent.absolute().joinpath('chrome-profile')}")

    # disable image loading for better performance
    # options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

    the_driver = webdriver.Chrome(executable_path=config.DRIVER_EXECUTABLE_PATH, options=options)

    # page loading time and wait time for page reload
    the_driver.set_page_load_timeout(5)
    the_driver.implicitly_wait(2)
    return the_driver


if __name__ == '__main__':
    with AutoLikeBot(configure_chrome_driver(),
                     post_filter=MyCustomFilter(ignore_tags=config.IGNORE_TAGS),
                     running_strategy=RunForeverWithBreaks(200)) as bot:
        bot.like_from_explore()
