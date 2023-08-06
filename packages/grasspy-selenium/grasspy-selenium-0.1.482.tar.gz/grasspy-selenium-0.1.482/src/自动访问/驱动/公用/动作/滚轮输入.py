从 selenium.webdriver.common.actions.wheel_input 导入 ScrollOrigin, WheelInput
从 汉化通用 导入 _反向注入

类 〇滚动原点(ScrollOrigin):
    
    @classmethod
    套路 从元素(本类, 元素, x偏移=0, y偏移=0):
        返回 本类(元素, x偏移, y偏移)
    
    @classmethod
    套路 从视口(本类, x偏移=0, y偏移=0):
        返回 本类("viewport", x偏移, y偏移)

    @property
    套路 原点(分身):
        返回 分身.origin
    
    @property
    套路 x偏移(分身):
        返回 分身.x_offset
    
    @property
    套路 y偏移(分身):
        返回 分身.y_offset

_反向注入(〇滚动原点, ScrollOrigin)


类 〇滚轮输入(WheelInput):

    套路 编码(分身):
        返回 分身.encode()

_反向注入(〇滚轮输入, WheelInput)