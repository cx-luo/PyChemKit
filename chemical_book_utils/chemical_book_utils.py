# -*- coding: utf-8 -*-
# @Time    : 2025/6/5 17:21
# @Author  : chengxiang.luo
# @Email   : chengxiang.luo@pharmaron.com
# @File    : chemical_book_utils.py
# @Software: PyCharm
import requests
from lxml import etree


def get_info_from_chemical_book(chem_name):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0',
        'Cookie': '_igp_14_=9a859f25-afca-4c54-bdd6-3d10b5abd6eb; _ga=GA1.2.1822275374.1708310930; _ga_WYVD9WP1XB=GS1.1.1716168212.18.0.1716168212.0.0.0; _ancsi_=CDFA2D8946F94D25A3056DEEB2E11F98; __ancsi_=CDFA2D8946F94D25A3056DEEB2E11F98; _ancsi_t_=F9C676F7D1F0E7AD1A9D71342A595E74; __ancsi_t_=F9C676F7D1F0E7AD1A9D71342A595E74; __root_domain_v=.chemicalbook.com; _qddaz=QD.610847289034848; Ketcher=0Chemicalbook39207-65-3.MOL%0a  Ketcher  5302516152D 1   1.00000     0.00000     0%0a%0a 12 12  0  0  0  0            999 V2000%0a    0.3572   -0.8250    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0%0a    0.3572    0.0000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0%0a    1.0717    0.4125    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0%0a    1.7862    0.0000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0%0a    1.7862   -0.8250    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0%0a    1.0717   -1.2375    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0%0a   -0.3572   -1.2375    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0%0a   -0.3572    0.4125    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0%0a   -1.0717    0.0000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0%0a   -1.0717   -0.8250    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0%0a   -0.3572    1.2375    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0%0a   -1.7862    0.4125    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0%0a  1  2  1  0     0  0%0a  2  3  1  0     0  0%0a  3  4  1  0     0  0%0a  4  5  1  0     0  0%0a  5  6  1  0     0  0%0a  1  6  1  0     0  0%0a  1  7  2  0     0  0%0a  8  9  1  0     0  0%0a  9 10  1  0     0  0%0a  8 11  2  0     0  0%0a  9 12  1  0     0  0%0a  2  8  1  0     0  0%0aM  END%0a; KetcherKey=9995f045a0a14890bf33062db2a45667; ASP.NET_SessionId=hrx4dlllc21xrmmjjd20nsvy; _gysszw=666666; Hm_lvt_7d450754590aa33d1fe40874160c2513=1748481763,1749088424; Hm_lpvt_7d450754590aa33d1fe40874160c2513=1749088424; HMACCOUNT=0479176E4AC88A75',
    }

    params = {
        'keyword': chem_name,
    }

    response = requests.get(
        f'https://www.chemicalbook.com/Search_EN.aspx',
        params=params, headers=headers
    )
    urls = etree.HTML(response.content.decode('utf-8'))
    # for url in urls:
    en_name = urls.xpath('//*[@class="mbox"]/tr[2]/td[2]/a/text()')
    mol_weight = urls.xpath('//*[@class="mbox"]/tr[5]/td[2]/text()')
    cas_no = urls.xpath('//*[@class="mbox"]/tr[6]/td[2]/text()')
    return en_name, mol_weight, cas_no


def get_density_from_chemical_book(key_words:str):
    cookies = {
        '_igp_14_': '9a859f25-afca-4c54-bdd6-3d10b5abd6eb',
        '_ga': 'GA1.2.1822275374.1708310930',
        '_ga_WYVD9WP1XB': 'GS1.1.1716168212.18.0.1716168212.0.0.0',
        '_ancsi_': 'CDFA2D8946F94D25A3056DEEB2E11F98',
        '__ancsi_': 'CDFA2D8946F94D25A3056DEEB2E11F98',
        '_ancsi_t_': 'F9C676F7D1F0E7AD1A9D71342A595E74',
        '__ancsi_t_': 'F9C676F7D1F0E7AD1A9D71342A595E74',
        '__root_domain_v': '.chemicalbook.com',
        '_qddaz': 'QD.610847289034848',
        'ASP.NET_SessionId': 'hrx4dlllc21xrmmjjd20nsvy',
        '_gysszw': '666666',
        'HMACCOUNT': '0479176E4AC88A75',
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        # 'Referer': 'https://www.chemicalbook.com/Search_EN.aspx?keyword=1,3-dioxolan-2-one',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0',
        'sec-ch-ua': '"Chromium";v="136", "Microsoft Edge";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        # 'Cookie': '_igp_14_=9a859f25-afca-4c54-bdd6-3d10b5abd6eb; _ga=GA1.2.1822275374.1708310930; _ga_WYVD9WP1XB=GS1.1.1716168212.18.0.1716168212.0.0.0; _ancsi_=CDFA2D8946F94D25A3056DEEB2E11F98; __ancsi_=CDFA2D8946F94D25A3056DEEB2E11F98; _ancsi_t_=F9C676F7D1F0E7AD1A9D71342A595E74; __ancsi_t_=F9C676F7D1F0E7AD1A9D71342A595E74; __root_domain_v=.chemicalbook.com; _qddaz=QD.610847289034848; Ketcher=0Chemicalbook39207-65-3.MOL%0a  Ketcher  5302516152D 1   1.00000     0.00000     0%0a%0a 12 12  0  0  0  0            999 V2000%0a    0.3572   -0.8250    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0%0a    0.3572    0.0000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0%0a    1.0717    0.4125    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0%0a    1.7862    0.0000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0%0a    1.7862   -0.8250    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0%0a    1.0717   -1.2375    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0%0a   -0.3572   -1.2375    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0%0a   -0.3572    0.4125    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0%0a   -1.0717    0.0000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0%0a   -1.0717   -0.8250    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0%0a   -0.3572    1.2375    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0%0a   -1.7862    0.4125    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0%0a  1  2  1  0     0  0%0a  2  3  1  0     0  0%0a  3  4  1  0     0  0%0a  4  5  1  0     0  0%0a  5  6  1  0     0  0%0a  1  6  1  0     0  0%0a  1  7  2  0     0  0%0a  8  9  1  0     0  0%0a  9 10  1  0     0  0%0a  8 11  2  0     0  0%0a  9 12  1  0     0  0%0a  2  8  1  0     0  0%0aM  END%0a; KetcherKey=9995f045a0a14890bf33062db2a45667; ASP.NET_SessionId=hrx4dlllc21xrmmjjd20nsvy; _gysszw=666666; Hm_lvt_7d450754590aa33d1fe40874160c2513=1748481763,1749088424; Hm_lpvt_7d450754590aa33d1fe40874160c2513=1749088424; HMACCOUNT=0479176E4AC88A75',
    }

    params = {
        'keyword': key_words,
    }

    response = requests.get(
        f'https://www.chemicalbook.com/Search_EN.aspx',
        params=params, cookies=cookies, headers=headers
    )

    print(response.status_code)
