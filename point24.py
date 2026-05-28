#!/usr/bin/python3 -u
# -*- encoding: utf-8 -*-
'''
@File          :   point24.py
@Time          :   2026/05/28 10:00:00
@Author        :   way-on
@Version       :   1.0
@Contact       :   i_chip_backend@163.com
@WebSite       :   https://blog.csdn.net/i_chip_backend
@License       :   (C)Copyright 2018-2026, ICerDev
@Description   :   24点游戏求解器 - 输入4个数字，用+-*/找出所有能得到24的表达式
'''

import argparse
import itertools as it
from fractions import Fraction
import time


def calc(x, y, op):
    """执行二元运算，除法使用 Fraction 避免浮点精度问题"""
    if x is None or y is None:
        return None
    if op == '+':
        return x + y
    elif op == '-':
        return x - y
    elif op == '*':
        return x * y
    elif op == '/':
        if y == 0:
            return None
        return Fraction(x, y)


# 5 种运算树结构的求值模板（对应 (((ab)c)d)、((a(bc))d) 等）
TEMPLATES = [
    lambda a, b, c, d, ops: calc(calc(calc(a, b, ops[0]), c, ops[1]), d, ops[2]),
    lambda a, b, c, d, ops: calc(calc(a, calc(b, c, ops[1]), ops[0]), d, ops[2]),
    lambda a, b, c, d, ops: calc(a, calc(calc(b, c, ops[1]), d, ops[2]), ops[0]),
    lambda a, b, c, d, ops: calc(calc(a, b, ops[0]), calc(c, d, ops[2]), ops[1]),
    lambda a, b, c, d, ops: calc(a, calc(b, calc(c, d, ops[2]), ops[1]), ops[0]),
]

# 运算符优先级
PREC = {'+': 1, '-': 1, '*': 2, '/': 2}


def to_string(node, parent_op=None, side=None):
    """将表达式树转换为字符串，按优先级自动添加括号"""
    if not isinstance(node, tuple):
        return str(node)
    op, left, right = node
    left_s = to_string(left, op, 'left')
    right_s = to_string(right, op, 'right')
    result = f'{left_s} {op} {right_s}'
    if parent_op is not None:
        child_p = PREC[op]
        parent_p = PREC[parent_op]
        if child_p < parent_p:
            result = f'({result})'
        elif child_p == parent_p and side == 'right' and parent_op in ('-', '/'):
            result = f'({result})'
    return result


# 5 种运算树结构的表达式树生成（与 TEMPLATES 一一对应）
TREES = [
    lambda a, b, c, d, ops: (ops[2], (ops[1], (ops[0], a, b), c), d),
    lambda a, b, c, d, ops: (ops[2], (ops[0], a, (ops[1], b, c)), d),
    lambda a, b, c, d, ops: (ops[0], a, (ops[2], (ops[1], b, c), d)),
    lambda a, b, c, d, ops: (ops[1], (ops[0], a, b), (ops[2], c, d)),
    lambda a, b, c, d, ops: (ops[0], a, (ops[1], b, (ops[2], c, d))),
]


def _get_terms(node, sign=1):
    """展开加减法表达式为 (符号, 项) 列表，用于标准化"""
    if not isinstance(node, tuple):
        return [(sign, str(node))]
    op, left, right = node
    if op == '+':
        return _get_terms(left, sign) + _get_terms(right, sign)
    elif op == '-':
        return _get_terms(left, sign) + _get_terms(right, -sign)
    else:
        return [(sign, canonical(node))]


def _get_factors(node, numerator=True):
    """展开乘除法表达式为 (分子/分母, 因子) 列表，用于标准化"""
    if not isinstance(node, tuple):
        return [(numerator, str(node))]
    op, left, right = node
    if op == '*':
        return _get_factors(left, numerator) + _get_factors(right, numerator)
    elif op == '/':
        return _get_factors(left, numerator) + _get_factors(right, not numerator)
    else:
        return [(numerator, canonical(node))]


def _rebuild_factors(factors):
    """将因子列表重新构建为规范化的乘除表达式字符串"""
    num = sorted(s for n, s in factors if n)
    den = sorted(s for n, s in factors if not n)

    if not num:
        num_str = '1'
    else:
        num_str = num[0]
        for s in num[1:]:
            num_str = f'({num_str} * {s})'

    if not den:
        return num_str

    den_str = den[0]
    for s in den[1:]:
        den_str = f'({den_str} * {s})'

    return f'({num_str} / {den_str})'


def _rebuild_terms(terms):
    """将项列表重新构建为规范化的加减表达式字符串"""
    terms.sort(key=lambda t: t[1])
    first_sign, first_s = terms[0]
    result = f'-{first_s}' if first_sign == -1 else first_s
    for sign, term_s in terms[1:]:
        if sign == 1:
            result = f'({result} + {term_s})'
        else:
            result = f'({result} - {term_s})'
    return result


def canonical(node):
    """表达式标准化：利用交换律/结合律将表达式转为规范形式用于去重"""
    if not isinstance(node, tuple):
        return str(node)
    op = node[0]

    if op in ('+', '-'):
        return _rebuild_terms(_get_terms(node))
    if op in ('*', '/'):
        return _rebuild_factors(_get_factors(node))

    return None


def point24_solve(numbers):
    """求解 24 点：遍历所有排列、运算符组合和树结构，返回去重后的表达式列表"""
    ops = ['+', '-', '*', '/']
    solutions = {}
    seen = set()

    for a, b, c, d in it.permutations(numbers, 4):
        for o0 in ops:
            for o1 in ops:
                for o2 in ops:
                    op_list = (o0, o1, o2)
                    for idx in range(len(TEMPLATES)):
                        result = TEMPLATES[idx](a, b, c, d, op_list)
                        if result is not None and result == 24:
                            tree = TREES[idx](a, b, c, d, op_list)
                            key = canonical(tree)
                            if key not in seen:
                                seen.add(key)
                                expr = to_string(tree)
                                solutions[expr] = True
    return list(solutions.keys())


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='24点游戏求解器')
    parser.add_argument('numbers', nargs='*', type=int, help='4个数字，空格分隔')
    return parser.parse_args()


def main():
    """主函数：读取输入、求解并输出结果"""
    args = parse_args()
    if args.numbers:
        numbers = args.numbers
    else:
        raw = input('Please input 4 digits (space separated) as point24 input:\n')
        numbers = [int(x) for x in raw.split()]
    print(f'digits: {" ".join(map(str, numbers))}')

    start = time.time()
    solutions = point24_solve(numbers)
    elapsed = time.time() - start

    for i, expr in enumerate(solutions, 1):
        print(f'Solution {i}: {expr} = 24')

    print(f'Total {len(solutions)} results for input: {numbers} [Elapsed time: {elapsed:.3f}s]')


if __name__ == '__main__':
    main()
