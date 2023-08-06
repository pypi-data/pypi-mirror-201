从 selenium.webdriver.chrome.webdriver 导入 WebDriver
导入 自动访问.驱动.chromium.驱动
从 .选项 导入 Options

类 〇驱动(WebDriver):
    """控制 Chrome 驱动, 使您可以驱动浏览器.

    您需要从以下网址下载 ChromeDriver 可执行文件:
    http://chromedriver.storage.googleapis.com/index.html
    """

    套路 __init__(
        分身,
        端口=0,
        选项々=空,
        服务参数々=空,
        期望能力々=空,
        服务日志路径=空,
        chrome选项々=空,
        服务=空,
        保持活动=假,
    ):
        super().__init__(
            port=端口,
            options=选项々,
            service_args=服务参数々,
            desired_capabilities=期望能力々,
            service_log_path=服务日志路径,
            chrome_options=chrome选项々,
            service=服务,
            keep_alive=保持活动,
        )