# Instagram Auto Like Bot

The code for [Instagram Auto Like Bot with Python + Selenium](https://medium.com/@maxAvdyushkin/instagram-auto-like-bot-with-python-selenium-539b21d3212b) blog post

### What is it?

Instagram bot that emulates user actions to like posts from explore that satisfy filter criteria (see [filter.py](filter.py))

### Requirements

- `selenium`

### Getting Started

To get started:
- Download chrome driver from https://chromedriver.chromium.org/ for your OS. Make sure it matches your Chrome version
- Put username and password in config file
- Run chrome_runner.py

You can easily change the bot to use any driver supported by selenium, just change options object to match parameters to driver of your choice.

### Component description

- [Runner](chrome_runner.py): configures webdriver, reads config and calls bot’s functions
- [Bot](bot.py): the core code that will interact with pages through webdriver
- [Parser](post_parser.py): code for parsing explore content, individual posts and any other data. Transforms data into Python primitives
- [Filter](filter.py): determines whether the bot should like a post if it satisfies certain criteria
- [Tracker](tracker.py): tracks what posts bot liked, how many it liked/skipped and other stats
- [Strategy](strategy.py): defines when the bot should stop running or maybe it should never stop
