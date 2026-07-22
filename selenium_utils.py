import os

from dotenv import load_dotenv
from selenium import webdriver

load_dotenv()

CHROME_BINARY = os.getenv('CHROME_BINARY', '/usr/local/bin/google-chrome')
CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH', '/usr/local/bin/chromedriver')
CHROME_DISABLE_WEB_SECURITY = os.getenv('CHROME_DISABLE_WEB_SECURITY', '0').lower() in ('1', 'true', 'yes')
CHROME_PROXY = os.getenv('CHROME_PROXY', '')

def get_options(profile_path: str, incognito: bool = False):
    chrome_options = webdriver.ChromeOptions()
    # 指定绑定版本的chrome浏览器，防止主机的chrome浏览器升级后与chromedriver不匹配导致失败
    chrome_options.binary_location = CHROME_BINARY

    """capability选项"""
    # 开启chrome的性能日志
    chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    """experimental选项"""
    # 开关配置
    # 禁止弹出窗口，禁止chrome正受到自动测试软件的控制
    exclude_switches = ['disable-popup-blocking', 'enable-automation']
    chrome_options.add_experimental_option('excludeSwitches', exclude_switches)

    # 禁止 Chrome 的站点通知权限（Permission Prompt）
    prefs = {
        "profile.default_content_setting_values.notifications": 2
    }
    chrome_options.add_experimental_option("prefs", prefs)

    """argument选项"""
    # 禁止 Chrome 的站点通知权限（Permission Prompt）
    chrome_options.add_argument('--disable-notifications')
    # 通过bot.sannysoft.com的反bot测试
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    # 设置语言为英语，因为要查找英语内容，如不设置有时会变为中文，导致内容查找失败
    chrome_options.add_argument('--lang=en-US')
    # 在容器化（docker）、低内存环境中使用该选项降低对内存的消耗
    chrome_options.add_argument('--disable-dev-shm-usage')
    # 一个奇怪的错误，启动时chrome即奔溃，但在海外win-server机器上正常，需要加上该参数才能在本地win-10机器上正常运行
    chrome_options.add_argument('--no-sandbox')
    # 可以添加headless称为无头浏览器（不启动界面）
    # chrome_options.add_argument('--headless')
    # 配置 remote debug port，singlefile 可以利用已打开的 chrome 实例进行下载，无需在 singlefile 执行时重复配置这里所有的 chrome 参数
    chrome_options.add_argument('--remote-debugging-port=9222')
    # 提高 singlefile/trafilatura 抓正文的稳定性；但会被部分站点 WAF（如 dailymotion 的
    # CloudFront）识别为异常并返回 401，故默认关闭，仅在需要的 worker 通过环境变量开启。
    if CHROME_DISABLE_WEB_SECURITY:
        chrome_options.add_argument('--disable-web-security')
    # 即将过时，新浏览器使用 --disable-web-security 即可
    # chrome_options.add_argument('--disable-features=IsolateOrigins,site-per-process')
    # 代理配置。socks5:// 时 Chrome 会把 DNS 解析也交给代理（远程 DNS），.onion 才能由 tor 解析。
    # 为空则不设代理，走容器默认出网（宿主机 mihomo）。
    if CHROME_PROXY:
        chrome_options.add_argument(f'--proxy-server={CHROME_PROXY.split("|")[0]}')
        # windows 测试使用，容器化部署可忽略
        if len(CHROME_PROXY.split("|")) > 0:
            chrome_options.add_argument(CHROME_PROXY.split("|")[-1])
    # 开启匿名模式
    if incognito:
        chrome_options.add_argument('--incognito')

    # 确保 profile 目录存在（在调用处创建）
    os.makedirs(profile_path, exist_ok=True)
    chrome_options.add_argument("--user-data-dir={user_data_dir}".format(user_data_dir=profile_path))

    return chrome_options


def init_incognito_chrome_driver(profile_path: str):
    chrome_options = get_options(profile_path, incognito=True)

    # 可以在 cmd 中使用 wmic process where "name='chrome.exe'" get CommandLine 查看配置项是否生效
    incognito_driver = webdriver.Chrome(options=chrome_options)

    return incognito_driver


def init_chrome_driver(profile_path: str):
    chrome_options = get_options(profile_path)

    # 可以在 cmd 中使用 wmic process where "name='chrome.exe'" get CommandLine 查看配置项是否生效
    driver = webdriver.Chrome(options=chrome_options)

    return driver