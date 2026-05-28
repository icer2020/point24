import itertools as it
from fractions import Fraction
import time


def calc(x, y, op):
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


TEMPLATES = [
    lambda a, b, c, d, ops: calc(calc(calc(a, b, ops[0]), c, ops[1]), d, ops[2]),
    lambda a, b, c, d, ops: calc(calc(a, calc(b, c, ops[1]), ops[0]), d, ops[2]),
    lambda a, b, c, d, ops: calc(a, calc(calc(b, c, ops[1]), d, ops[2]), ops[0]),
    lambda a, b, c, d, ops: calc(calc(a, b, ops[0]), calc(c, d, ops[2]), ops[1]),
    lambda a, b, c, d, ops: calc(a, calc(b, calc(c, d, ops[2]), ops[1]), ops[0]),
]

FMT = [
    '(({a} {o0} {b}) {o1} {c}) {o2} {d}',
    '({a} {o0} ({b} {o1} {c})) {o2} {d}',
    '{a} {o0} (({b} {o1} {c}) {o2} {d})',
    '({a} {o0} {b}) {o1} ({c} {o2} {d})',
    '{a} {o0} ({b} {o1} ({c} {o2} {d}))',
]

TREES = [
    lambda a, b, c, d, ops: (ops[2], (ops[1], (ops[0], a, b), c), d),
    lambda a, b, c, d, ops: (ops[2], (ops[0], a, (ops[1], b, c)), d),
    lambda a, b, c, d, ops: (ops[0], a, (ops[2], (ops[1], b, c), d)),
    lambda a, b, c, d, ops: (ops[1], (ops[0], a, b), (ops[2], c, d)),
    lambda a, b, c, d, ops: (ops[0], a, (ops[1], b, (ops[2], c, d))),
]


def _get_terms(node, sign=1):
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
    if not isinstance(node, tuple):
        return str(node)
    op = node[0]

    if op in ('+', '-'):
        return _rebuild_terms(_get_terms(node))
    if op in ('*', '/'):
        return _rebuild_factors(_get_factors(node))

    return None


def point24_solve(numbers):
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
                                expr = FMT[idx].format(a=a, b=b, c=c, d=d, o0=o0, o1=o1, o2=o2)
                                solutions[expr] = True
    return list(solutions.keys())


def main():
    raw = input('Please input 4 digits (space separated) as point24 input:\n')
    numbers = [int(x) for x in raw.split()]
    print(f'digits: {raw}')

    start = time.time()
    solutions = point24_solve(numbers)
    elapsed = time.time() - start

    for i, expr in enumerate(solutions, 1):
        print(f'Solution {i}: ({expr}) = 24')

    print(f'Total {len(solutions)} results for input: {numbers} [Elapsed time: {elapsed:.3f}s]')


if __name__ == '__main__':
    main()
