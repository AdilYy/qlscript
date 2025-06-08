import requests
from datetime import datetime, timedelta
import time
from bs4 import BeautifulSoup
import os  # 环境变量支持
​
# --------------------- 环境变量配置 ---------------------
USER_INFO = os.getenv('USER_INFO', '').strip()  # 复合环境变量（必填）
​
# --------------------- 常量定义 ---------------------
INDEX_URL = "http://m.woread.com.cn/touchactivity/privilegeCenter/index.action?pageIndex=e9d413b7251d4722a676d8d1239226e5&channelid=18500001"
RECORD_URL = "http://m.woread.com.cn/touchactivity/privilegeCenter/record.action"
EXCHANGE_URL = "http://m.woread.com.cn/touchactivity/privilegeCenter/exchange.action"
COMMON_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 15; RMX3800 Build/UKQ1.231108.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/134.0.6998.136 Mobile Safari/537.36',
    'Referer': INDEX_URL,
}
EXCHANGE_PARAMS = {
    'pageIndex': 'e9d413b7251d4722a676d8d1239226e5',
    'partId': '2106',
    'isQq': '0'
}
​
# --------------------- 青龙内置通知函数 ---------------------
def send_notify(title, content):
    """使用青龙面板内置Notify.js发送通知"""
    try:
        import notify
        notify.send(title, content)
        print("[青龙通知] 发送成功")