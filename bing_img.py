#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author:pear
@license: Apache Licence 
@file: bing_img.py
@time: 2020/1/3 21:31
@contact: 1101588023@qq.com
@software: PyCharm

# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
"""

import os
import time
import requests
from lxml import etree

url_list = [
    'https://cn.bing.com/?FORM=BEHPTB',
    'https://cn.bing.com/?FORM=BEHPTB&ensearch=1'
]

today = time.strftime("%Y-%m-%d", time.localtime())


def get_img_url(url):
    r = requests.get(url)
    selector = etree.HTML(r.content)
    link = selector.xpath('//link[@id="bgLink"]/@href')
    if link:
        img_url = 'https://cn.bing.com/' + link[0]
        save_img(img_url)


def save_img(url):
    if 'ZH-CN' in url and '.jpg' in url:
        file = f'{today}_ZH-CN.jpg'
    elif 'EN-CN' in url and '.jpg' in url:
        file = f'{today}_EN-CN.jpg'
    else:
        return
    if os.path.isfile(file):
        print(f'pass: {file}')
        return
    else:
        r = requests.get(url)
        with open(file, 'wb') as f:
            f.write(r.content)
            print(f'save: {file}')


def main():
    for url in url_list:
        get_img_url(url)


if __name__ == '__main__':
    main()
    input('...')
