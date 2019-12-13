#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author:pear
@license: Apache Licence 
@file: tax_calc.py
@time: 2019/11/27 17:43
@contact: 1101588023@qq.com
@software: PyCharm

# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
"""

import re
import sys
from decimal import Decimal, ROUND_HALF_UP

ZH_HANS_MAP = dict(zip(range(10), "零壹贰叁肆伍陆柒捌玖"))


def verbose_price(cost):
    """convert price to zh_hans"""
    cost = Decimal(cost).quantize(Decimal('0.00'), ROUND_HALF_UP)  # 四舍五入保留两位小数
    if cost >= 100_000_000:
        return "大于等于1亿"
    if cost >= 10000:
        w = int(cost // 10000)
        rest = int(cost % 10000)
        r = qian(w) + "万" + qian(rest)
    elif cost >= 1:
        r = qian(int(cost))
    else:
        r = ""
    if r:
        r += "元"
    if int(cost) == cost:
        r += "整"
    else:
        j, f = int(cost * Decimal(10)) % 10, int(cost * Decimal(100)) % 10
        t = ZH_HANS_MAP[j] + "角" * bool(j) + ZH_HANS_MAP[f] + "分" * bool(f)
        t = t.rstrip("零")
        if not r:
            t = t.lstrip("零")
        r += t
    return re.sub(r"零{2,}", "零", r.strip("零"))


def qian(c):
    ds = [int(i) for i in list(f"{c:04}")]
    ts = list("仟佰拾") + [""]
    s = "".join(ZH_HANS_MAP[d] + t * bool(d) for d, t in zip(ds, ts))
    return s.rstrip("零")


def tax_calc(a):
    """
    :param a: 含税金额
    :return: b: 不含税金额, c: 税额
    """
    n = 0.03  # 税率
    b = a / (n + 1)
    c = b * n
    return f'{b:.2f}, {c:.2f}'


def main(argv):
    cost = float(argv)
    print(f'{cost:.2f}')
    print(verbose_price(cost))
    print(tax_calc(cost))


if __name__ == "__main__":
    main(sys.argv[1])
