从 selenium.webdriver.common.options 导入 BaseOptions, ArgOptions
从 汉化通用 导入 _反向注入

类 〇基本选项(BaseOptions):
    """具体浏览器选项的基类"""

    @property
    套路 能力々(分身):
        返回 分身.capabilities

    套路 设置能力(分身, 名称, 值):
        分身.set_capability(名称, 值)

_反向注入(〇基本选项, BaseOptions)


类 〇参数选项(ArgOptions):

    @property
    套路 参数々(分身):
        返回 分身.arguments

    套路 添加参数(分身, 参数):
        分身.add_argument(参数)

_反向注入(〇参数选项, ArgOptions)