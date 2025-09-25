# -*- coding: utf-8 -*-
# @Time    : 2025/6/20 9:26
# @Author  : chengxiang.luo
# @Email   : chengxiang.luo@pharmaron.com
# @File    : cas_database.py
# @Software: PyCharm

import json
import os
import time

import requests
from lxml import etree

from utils.logger import logger

# 缓存目录（可选）
CACHE_DIR = './.cas_cache'
os.makedirs(CACHE_DIR, exist_ok=True)
cookies = {
    '_igp_14_': '9a859f25-afca-4c54-bdd6-3d10b5abd6eb',
    '_ga_WYVD9WP1XB': 'GS1.1.1716168212.18.0.1716168212.0.0.0',
    '_ancsi_': 'CDFA2D8946F94D25A3056DEEB2E11F98',
    '__ancsi_': 'CDFA2D8946F94D25A3056DEEB2E11F98',
    '_ancsi_t_': 'F9C676F7D1F0E7AD1A9D71342A595E74',
    '__ancsi_t_': 'F9C676F7D1F0E7AD1A9D71342A595E74',
    '__root_domain_v': '.chemicalbook.com',
    '_qddaz': 'QD.610847289034848',
    'Hm_lvt_7d450754590aa33d1fe40874160c2513': '1748481763,1749088424',
    'ASP.NET_SessionId': 'ywkgpybeghah3ei20gbrjjok',
    '_gysszw': '666666',
    '_qddab': '3-ih8jox.mc36au43',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
    'sec-ch-ua': '"Microsoft Edge";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': '_igp_14_=9a859f25-afca-4c54-bdd6-3d10b5abd6eb; _ga_WYVD9WP1XB=GS1.1.1716168212.18.0.1716168212.0.0.0; _ancsi_=CDFA2D8946F94D25A3056DEEB2E11F98; __ancsi_=CDFA2D8946F94D25A3056DEEB2E11F98; _ancsi_t_=F9C676F7D1F0E7AD1A9D71342A595E74; __ancsi_t_=F9C676F7D1F0E7AD1A9D71342A595E74; __root_domain_v=.chemicalbook.com; _qddaz=QD.610847289034848; Hm_lvt_7d450754590aa33d1fe40874160c2513=1748481763,1749088424; ASP.NET_SessionId=ywkgpybeghah3ei20gbrjjok; _gysszw=666666; _qddab=3-ih8jox.mc36au43',
}


def get_cas_database(page_num, use_cache=False):
    """
    获取 CAS 数据列表（带缓存和错误处理）
    :param page_num: 分页编号
    :param use_cache: 是否启用缓存
    :return: 化学试剂列表 [cas_str, ref, reagent_name, reagent_formula]
    """
    cache_path = os.path.join(CACHE_DIR, f"page_{page_num}.json")

    if use_cache and os.path.exists(cache_path):
        logger.info(f"Loading from cache: {cache_path}")
        with open(cache_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    url = f'https://www.chemicalbook.com/CASDetailList_{page_num}_EN.htm'

    try:
        logger.info(f"Fetching URL: {url}")
        response = requests.get(url, headers=headers, cookies=cookies, timeout=100)
        response.raise_for_status()  # 检查响应状态码
        time.sleep(1)  # 控制频率，防止被封IP

        html = etree.HTML(response.content.decode('utf-8'))
        table = html.xpath('//*[@id="ContentPlaceHolder1_ProductClassDetail"]')

        if not table:
            logger.warning(f"No table found on page {page_num}")
            return []

        _reagent_list = []
        rows = table[0].xpath('.//tr')[1:]  # 跳过表头

        for row in rows:
            cas_node = row.xpath('./td[1]/a')
            name_node = row.xpath('./td[2]/a')
            if not cas_node:
                continue

            try:
                _cas_str = cas_node[0].text.strip()
                _cas_ref = 'https://www.chemicalbook.com' + cas_node[0].get('href').strip()
                _reagent_name = name_node[0].text.strip()
                _reagent_name_ref = 'https://www.chemicalbook.com' + name_node[0].get('href').strip()
                _reagent_formula = row.xpath('./td[3]/span/text()')[0].strip()

                _reagent_list.append([_cas_str, _cas_ref, _reagent_name, _reagent_name_ref, _reagent_formula])
            except Exception as e:
                logger.warning(f"Error parsing row: {e}")
                continue

        # 写入缓存
        if use_cache:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(_reagent_list, f, ensure_ascii=False, indent=2)

        return _reagent_list

    except requests.RequestException as e:
        logger.error(f"Network error fetching page {page_num}: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error on page {page_num}: {e}")
        return []
