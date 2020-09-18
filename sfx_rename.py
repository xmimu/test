#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author:pear
@file: sfx_rename.py
@time: 2020/9/17 18:52
@contact: 1101588023@qq.com
@software: PyCharm
"""

import os
from glob import glob
import re
from decimal import Decimal

"""
使用：
导出整段的父region，region名必须带有"full"，这是判断依据；
导出包含的子region，如果带序号"01", "02"请写进region名，程序不包含排序；
导出通配符用 "$region_[$start&$end]"，通过头尾判断包含关系；
把脚本添加到环境变量，在需要处理的目录cmd调用，或者把脚本放到处理的目录下运行。
"""

main_path = os.getcwd()


def get_file_data(path):
    file_data = []
    for file in glob(f'{path}/*.wav'):
        res = re.search(r'\[0-(\d\d\.\d+)&0-(\d\d\.\d+)\]\.wav', file)
        if res:
            start, end = res.groups()
            file_data.append({
                'file': file,
                'file_name': os.path.split(file)[1],
                'start': float(start),
                'end': float(end)
            })
    return file_data


def parse_file_data(file_data):
    for i in file_data:
        if 'full' in i['file'].lower():
            start = Decimal(str(i['start']))
            print(f'new_start: {start}')
            new_file = re.sub(r'\[0-(\d\d\.\d+)&0-(\d\d\.\d+)\]', str(start), i['file'])
            print(f'new_file: {new_file}')
            os.rename(i['file'], new_file)
        else:
            continue

        for j in file_data:
            if i == j:
                continue
            if j['start'] >= i['start'] and j['end'] <= i['end']:
                # i 包含 j, 修改 j
                print(f'{j["file_name"]} in {i["file_name"]}')
                start = Decimal(str(j['start'])) - Decimal(str(i['start']))
                print(f'new_start: {start}')
                new_file = re.sub(r'\[0-(\d\d\.\d+)&0-(\d\d\.\d+)\]', str(start), j['file'])
                print(f'new_file: {new_file}')
                os.rename(j['file'], new_file)


def main():
    file_data = get_file_data(main_path)
    parse_file_data(file_data)


if __name__ == '__main__':
    main()
