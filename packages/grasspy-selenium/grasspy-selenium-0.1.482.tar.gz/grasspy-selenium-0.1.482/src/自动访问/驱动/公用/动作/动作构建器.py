从 selenium.webdriver.common.actions.action_builder 导入 ActionBuilder
从 .指针动作 导入 〇指针动作
从 汉化通用 导入 _反向注入

类 〇动作构建器(ActionBuilder):

    @property
    套路 按键动作(分身):
        返回 分身.key_action
    
    @property
    套路 指针动作(分身):
        返回 分身.pointer_action
    
    @property
    套路 滚轮动作(分身):
        返回 分身.wheel_action
    
    套路 完成(分身):
        分身.perform()

    套路 清空动作(分身):
        分身.clear_actions()

_反向注入(〇动作构建器, ActionBuilder)