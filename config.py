import pathlib

USERNAME = ''  # instagram account

PASSWORD = ''  # instagram password

# executable path for chrome driver
DRIVER_EXECUTABLE_PATH = pathlib.Path(__file__).parent.absolute().joinpath("chromedriver")

IGNORE_TAGS = []  # exact case non sensitive matching

SKIP_LOGIN = False  # skip log in flow. Useful if you have profile with cookies saved
