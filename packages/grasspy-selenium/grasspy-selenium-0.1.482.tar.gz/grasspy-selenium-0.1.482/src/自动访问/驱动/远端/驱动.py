从 selenium.webdriver.remote.webdriver 导入 WebDriver
导入 自动访问.驱动.远端.切换到
导入 自动访问.驱动.远端.网页元素
从 自动访问.驱动.公用.依据 导入 〇依据
从 汉化通用 导入 _反向注入

类 〇驱动(WebDriver):

    @property
    套路 名称(分身):
        返回 分身.name

    套路 开始会话(分身, 能力々, 浏览器配置文件=空):
        分身.start_session(能力々)

    套路 创建web元素(分身, 元素id):
        返回 分身.create_web_element(元素id)

    套路 执行命令(分身, 驱动命令, 参数々=空):
        返回 分身.execute(驱动命令, 参数々)

    套路 获取(分身, url):
        """在当前浏览器会话中加载一个网页"""
        分身.execute("get", {"url": url})

    @property
    套路 抬头(分身):
        返回 分身.title

    套路 执行脚本(分身, 脚本, *参数々):
        返回 分身.execute_script(脚本, *参数々)
    
    套路 执行异步脚本(分身, 脚本, *参数々):
        返回 分身.execute_async_script(脚本, *参数々)

    @property
    套路 当前url(分身):
        返回 分身.current_url
    
    @property
    套路 网页源代码(分身):
        返回 分身.page_source

    套路 关闭(分身):
        分身.execute("close")
    
    套路 退出(分身):
        分身.quit()

    @property
    套路 当前窗口句柄(分身):
        返回 分身.current_window_handle
    
    @property
    套路 窗口句柄々(分身):
        返回 分身.window_handles

    套路 窗口最大化(分身):
        分身.maximize_window()
    
    套路 窗口全屏(分身):
        分身.fullscreen_window()
    
    套路 窗口最小化(分身):
        分身.minimize_window()

    套路 打印网页(分身, 打印选项々=空):
        返回 分身.print_page(打印选项々)

    @property
    套路 切换到(分身):
        返回 分身.switch_to

    套路 后退(分身):
        分身.back()
    
    套路 前进(分身):
        分身.forward()
    
    套路 刷新(分身):
        分身.refresh()

    套路 获取酷卡々(分身):
        返回 分身.get_cookies()
    
    套路 获取酷卡(分身, 名称):
        返回 分身.get_cookie(名称)
    
    套路 删除酷卡(分身, 名称):
        分身.delete_cookie(名称)
    
    套路 删除所有酷卡(分身):
        分身.delete_all_cookies(名称)
    
    套路 添加酷卡(分身, 酷卡字典):
        分身.add_cookie(酷卡字典)
    
    套路 隐式等待(分身, 等待时间):
        分身.implicitly_wait(等待时间)

    套路 设置脚本超时(分身, 等待时间):
        分身.set_script_timeout(等待时间)
    
    套路 设置网页加载超时(分身, 等待时间):
        分身.set_page_load_timeout(等待时间)

    @property
    套路 超时々(分身):
        返回 分身.timeouts
    
    @超时々.setter
    套路 超时々(分身, 超时々):
        _ = 分身.execute("setTimeouts", 超时々._to_json())["value"]

    套路 查找元素(分身, 依据=〇依据.ID, 值=空):
        返回 分身.find_element(by=依据, value=值)
    
    套路 查找元素々(分身, 依据=〇依据.ID, 值=空):
        返回 分身.find_elements(by=依据, value=值)

    @property
    套路 能力々(分身):
        返回 分身.capabilities

    套路 屏幕截图保存为文件(分身, 文件名):
        返回 分身.get_screenshot_as_file(文件名)
    
    套路 保存屏幕截图(分身, 文件名):
        返回 分身.save_screenshot(文件名)

    套路 获取屏幕截图_png(分身):
        返回 分身.get_screenshot_as_png()
    
    套路 获取屏幕截图_base64(分身):
        返回 分身.get_screenshot_as_base64()

    套路 设置窗口尺寸(分身, 宽度, 高度, 窗口句柄="current"):
        分身.set_window_size(宽度, 高度, windowHandle=窗口句柄)
    
    套路 获取窗口尺寸(分身, 窗口句柄="current"):
        返回 分身.get_window_size(windowHandle=窗口句柄)
    
    套路 设置窗口位置(分身, x, y, 窗口句柄="current"):
        返回 分身.set_window_position(x, y, windowHandle=窗口句柄)
    
    套路 获取窗口位置(分身, 窗口句柄="current"):
        返回 分身.get_window_position(windowHandle=窗口句柄)
    
    套路 设置窗口矩形(分身, x=空, y=空, 宽度=空, 高度=空):
        返回 分身.set_window_rect(x=x, y=y, width=宽度, height=高度)
    
    套路 获取窗口矩形(分身):
        返回 分身.get_window_rect()

_反向注入(〇驱动, WebDriver)