#!/usr/bin/env python3
# @author Adil
# 更新日期：2025-03-08
# 仓库地址：https://github.com/AdilYy/qlscript.git
# 感谢Viki开源的的API接口

import requests
import notify
import logging
from datetime import datetime

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

API_URL = 'https://60s-api.viki.moe/v2/60s'

def get_60s_data():
    """获取并处理60秒数据（带重试机制）"""
    retry = 0
    while retry < 3:
        try:
            resp = requests.get(API_URL, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            
            if data.get('code') != 200:
                raise ValueError(f"API状态码异常：{data.get('message', '未知错误')}")
                
            news_data = data['data']
            return {
                'date': news_data.get('date', datetime.now().strftime("%Y-%m-%d")),
                'news': news_data.get('news', [])
            }
            
        except requests.exceptions.RequestException as e:
            logging.warning(f"网络请求失败，正在重试...（{retry+1}/3）")
            retry += 1
        except Exception as e:
            logging.error(f"数据处理失败：{str(e)}")
            return None
    return None

def format_html(news_info):
    """生成带样式的HTML内容"""
    html_content = [
        f"<b>📅 {news_info['date']} 60秒看世界 🌍</b>",
        "<hr style='border: 1px solid #e0e0e0; margin: 12px 0;'>"
    ]
    
    for idx, item in enumerate(news_info['news'], 1):
        # 处理不同数据格式
        if isinstance(item, dict):
            title = item.get('title', '').strip()
            content = item.get('content', '').strip()
            line = f"{idx}. <b>{title}</b><br>{content}"
        else:
            line = f"{idx}. {str(item).strip()}"
        
        # 替换换行符并添加分割线
        line = line.replace('\n', '<br>')
        html_content.append(f"{line}<br><div style='border-bottom: 1px dashed #f0f0f0; margin: 8px 0;'></div>")
    
    return "".join(html_content)

def main():
    logging.info("开始获取60秒资讯...")
    news_data = get_60s_data()
    
    if not news_data or not news_data.get('news'):
        logging.error("获取内容失败，请检查网络或API状态")
        return
    
    # 生成带样式的HTML内容
    html_content = format_html(news_data)
    
    # 发送推送（适配支持HTML的通知渠道）
    notify.send(
        title="60秒看世界",
        content=html_content,
        html=True  # 启用HTML格式支持
    )
    logging.info("推送已完成")

if __name__ == '__main__':
    main()