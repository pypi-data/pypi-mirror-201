从 selenium.webdriver.edge.webdriver 导入 WebDriver
导入 自动访问.驱动.chromium.驱动
从 .选项 导入 Options

类 〇驱动(WebDriver):
    """控制 Microsoft Edge 驱动, 使您可以驱动浏览器.

    您需要从以下网址下载 MSEdgeDriver (Chromium) 可执行文件:
    https://developer.microsoft.com/en-us/microsoft-
    edge/tools/webdriver/
    """

    套路 __init__(
        分身,
        端口=0,
        选项々=Options(),
        服务参数々=空,
        能力々=空,
        服务日志路径=空,
        服务=空,
        保持活动=假,
        冗长=假,
    ):
        super().__init__(
            port=端口,
            options=选项々,
            service_args=服务参数々,
            capabilities=能力々,
            service_log_path=服务日志路径,
            service=服务,
            keep_alive=保持活动,
            verbose=冗长,
        )

    套路 创建选项々(分身):
        返回 Options()