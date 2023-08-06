从 selenium.webdriver.common.actions.wheel_actions 导入 WheelActions
从 汉化通用 导入 _反向注入


类 〇滚轮动作(WheelActions):

    套路 暂停(分身, 时长=0):
        返回 分身.pause(时长)

    套路 滚动(分身, x=0, y=0, x距离=0, y距离=0, 时长=0, 原点="viewport"):
        返回 分身.scroll(x=x, y=y, delta_x=x距离, delta_y=y距离, duration=时长, origin=原点)

_反向注入(〇滚轮动作, WheelActions)