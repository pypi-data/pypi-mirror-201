从 selenium.webdriver.remote.webelement 导入 WebElement
# 导入 切换到
从 自动访问.驱动.公用.依据 导入 〇依据
从 汉化通用 导入 _反向注入

类 〇网页元素(WebElement):

    @property
    套路 标签名(分身):
        返回 分身.tag_name
    
    @property
    套路 文本(分身):
        返回 分身.text

    套路 点击(分身):
        分身.click()
    
    套路 提交(分身):
        分身.submit()
    
    套路 清空(分身):
        分身.clear()
    
    套路 获取属性(分身, 名称):
        返回 分身.get_property(名称)
    
    套路 获取dom属性(分身, 名称):
        返回 分身.get_dom_attribute(名称)
    
    套路 获取特性(分身, 名称):
        返回 分身.get_attribute(名称)

    套路 已选中(分身):
        返回 分身.is_selected()
    
    套路 已启用(分身):
        返回 分身.is_enabled()
    
    套路 发送按键(分身, *值):
        分身.send_keys(*值)

    @property
    套路 影子根(分身):
        返回 分身.shadow_root

    套路 已显示(分身):
        返回 分身.is_displayed()

    @property
    套路 尺寸(分身):
        返回 分身.size

    套路 css属性值(分身):
        返回 分身.value_of_css_property()

    @property
    套路 位置(分身):
        返回 分身.location
    
    @property
    套路 矩形(分身):
        返回 分身.rect
    
    @property
    套路 屏幕截图_png(分身):
        返回 分身.screenshot_as_png
    
    @property
    套路 屏幕截图_base64(分身):
        返回 分身.screenshot_as_base64

    套路 屏幕截图(分身, 文件名):
        返回 分身.screenshot(文件名)

    套路 查找元素(分身, 依据=〇依据.ID, 值=空):
        返回 分身.find_element(by=依据, value=值)
    
    套路 查找元素々(分身, 依据=〇依据.ID, 值=空):
        返回 分身.find_elements(by=依据, value=值)

_反向注入(〇网页元素, WebElement)