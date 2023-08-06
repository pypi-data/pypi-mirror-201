从 selenium.webdriver.remote.switch_to 导入 SwitchTo
从 汉化通用 导入 _反向注入

类 〇切换到(SwitchTo):

    @property
    套路 活动元素(分身):
        返回 分身.active_element
    
    @property
    套路 警示(分身):
        返回 分身.alert

    套路 默认内容(分身):
        分身.default_content()

    套路 框架(分身, 框架参考):
        分身.frame(框架参考)

    套路 新窗口(分身, 类型提示=空):
        分身.new_window(类型提示)

    套路 父框架(分身):
        分身.parent_frame()

    套路 窗口(分身, 窗口名称):
        分身.window(窗口名称)

_反向注入(〇切换到, SwitchTo)