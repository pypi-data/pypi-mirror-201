从 selenium.webdriver.edge.service 导入 Service

类 〇服务(Service):
    """服务对象负责启动和停止 Edge 驱动"""

    套路 __init__(
        分身,
        可执行文件路径="msedgedriver",
        端口=0,
        冗长=假,
        日志路径=空,
        服务参数々=空,
        环境=空,
    ):
        super().__init__(
            executable_path=可执行文件路径,
            port=端口,
            verbose=冗长,
            log_path=日志路径,
            service_args=服务参数々,
            env=环境,
        )