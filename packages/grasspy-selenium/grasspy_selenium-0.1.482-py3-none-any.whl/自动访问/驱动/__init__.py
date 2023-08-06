from selenium.webdriver.chromium.webdriver import ChromiumDriver

套路 __退出(分身):
    分身.quit()

ChromiumDriver.退出 = __退出

from .chrome.选项 import Options as Chrome选项
from .chrome.驱动 import 〇驱动 as Chrome
from .公用.动作链 import 〇动作链
# from .公用.desired_capabilities import DesiredCapabilities
from .公用.按键 import 〇按键
# from .公用.proxy import Proxy
from .edge.选项 import Options as Edge选项
from .edge.驱动 import 〇驱动 as Edge

__all__ = [
    "Chrome选项",
    "Chrome",
    "〇动作链",
    # "DesiredCapabilities",
    "〇按键",
    # "Proxy",
    "Edge选项",
    "Edge",
]