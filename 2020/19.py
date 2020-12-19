import re


def parse_rule(rule_str):
    _id, result = rule_str.strip().split(':')
    _id = int(_id)
    alternatives = [[int(y) if y.isnumeric() else y for y in x.strip().split(' ')] for x in result.split('|')]
    return _id, alternatives


def build_regex(rules, current_symbol, depth, max_depth):
    if current_symbol not in rules:
        return current_symbol.replace('"', '')

    s = '|'.join(
        ''.join(
            build_regex(rules, symbol, depth + 1, max_depth)
            for symbol in alt
        )
        for alt in rules[current_symbol]
        if current_symbol not in alt or depth < max_depth
    )
    return f'({s})' if len(s) > 1 else s


with open('19.in') as f:
    rule_lines, messages = f.read().split('\n\n')
    rule_lines = rule_lines.replace('8: 42', '8: 42 | 42 8')
    rule_lines = rule_lines.replace('11: 42 31', '11: 42 31 | 42 11 31')
    rule_lines = rule_lines.split('\n')
    messages = messages.split('\n')

    rules = {}
    for r in rule_lines:
        rule_id, rule = parse_rule(r)
        rules[rule_id] = rule

    reg = re.compile('^' + build_regex(rules, 0, 0, max(map(len, messages))) + '$')
    print(len(list(filter(lambda x: x is not None, [re.match(reg, m) for m in messages]))))
