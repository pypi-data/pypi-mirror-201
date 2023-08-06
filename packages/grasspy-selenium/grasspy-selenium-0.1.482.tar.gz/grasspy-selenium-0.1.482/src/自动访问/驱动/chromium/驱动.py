从 selenium.webdriver.chromium.webdriver 导入 ChromiumDriver
导入 自动访问.驱动.远端.驱动
从 汉化通用 导入 _反向注入

类 Chromium驱动(ChromiumDriver):

    套路 获取网络条件々(分身):
        返回 分身.get_network_conditions()
    
    套路 设置网络条件々(分身, *网络条件々):
        返回 分身.set_network_conditions(*网络条件々)
    
    套路 删除网络条件々(分身):
        分身.delet_network_conditions()

_反向注入(Chromium驱动, ChromiumDriver)