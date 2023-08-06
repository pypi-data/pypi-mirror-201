从 selenium.webdriver.chrome.service 导入 Service

类 〇服务(Service):
    """服务对象负责启动和停止 Chrome 驱动"""

    套路 __init__(
        分身,
        可执行文件路径="chromedriver",
        端口=0,
        服务参数々=空,
        日志路径=空,
        环境=空,
    ):
        super().__init__(
            executable_path=可执行文件路径,
            port=端口,
            service_args=服务参数々,
            log_path=日志路径,
            env=环境,
        )